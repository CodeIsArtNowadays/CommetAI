import json
import uuid
import httpx
import hmac
import hashlib

from typing_extensions import List

from src.auth.models import User
from src.ai.service import AiService
from src.board.models import Project
from src.board.repository import CommitRepository, ProjectRepository
from src.board.schemas import (
    ProjectCreateRequestSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    WebhookDataCreateSchema,
    CommitCreateSchema
)
from src.core.exceptions import (
    ProjectAccessIsNotAllowedException,
    ProjectNotFoundException,
    GithubUnAutharize,
    GithubApiException
)


class ProjectService:
    def __init__(self, repo: ProjectRepository, webhook_service: WebhookService):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.webhook_service = webhook_service
            
    async def create_project(
        self, project_schema: ProjectCreateRequestSchema, user: User
    ) -> Project:
        project_complete_schema = ProjectCreateSchema(
            **project_schema.model_dump(), owner_id=user.id
        )
        project = await self.repo.create_project(project_complete_schema)
        repo_full_name = project.owner.username + '/' + project.title
        
        wh_data_raw = await self.webhook_service.create_webhook(repo_full_name, user.github_token)
        
        wh_data = WebhookDataCreateSchema(
            webhook_id=wh_data_raw['wh_id'],
            webhook_secret=wh_data_raw['secret'],
            repo_full_name=repo_full_name
        )
        
        project = await self.repo.set_wh_data(project, wh_data)
        
        return project
    
    async def _get_project_or_403(self, project_id: int, user_id: int) -> Project:
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundException()
        if not project.owner_id == user_id:
            raise ProjectAccessIsNotAllowedException()
        return project

    async def get_project_by_id(self, project_id: int, user_id: int) -> Project:
        return await self._get_project_or_403(project_id, user_id)

    async def get_all_project_by_user(self, user_id: int) -> list[Project]:
        res = await self.repo.get_all_project_by_user(user_id)
        return list(res)

    async def update_project(
        self, project_id: int, update_project: ProjectUpdateSchema, user_id: int
    ) -> Project:
        await self._get_project_or_403(project_id, user_id)
        return await self.repo.update_project(project_id, update_project)

    async def delete_project(self, project_id: int, user_id: int) -> None:
        await self._get_project_or_403(project_id, user_id)
        await self.repo.delete_project(project_id)


class WebhookService:
    
    def __init__(self, ai_service: AiService, commit_repo: CommitRepository):
        self.ai_service = ai_service
        self.commit_repo = commit_repo
        
    async def create_webhook(self, repo_full_name: str, owner_github_token: str):
        
        url = f'https://api.github.com/repos/{repo_full_name}/hooks'
        headers = {
            'Authorization': f'Bearer {owner_github_token}',
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        secret = str(uuid.uuid4())
        
        async with httpx.AsyncClient() as client:
            
            response = await client.post(
                url,
                headers=headers,
                json={
                    'name': 'web',
                    'active': True,
                    'events': ['push'],
                    'config': {
                        'secret': secret,
                        'url': 'https://peddling-unsure-unpaid.ngrok-free.dev/webhook/event',
                        'content_type': 'json'
                    }
                }
            )
            
            if not response.status_code == 201:
                raise GithubApiException(response.status_code)
                
            response_data = response.json()
            return {
                'wh_id': response_data['id'],
                'secret': secret
            }
            
    async def get_commits_from_webhook(self, commits: List, repo_full_name: str, owner_github_token: str):
        res = []
        async with httpx.AsyncClient() as client:
            for commit in commits:
                commit_id = commit['id']
                
                
                url = f'https://api.github.com/repos/{repo_full_name}/commits/{commit_id}'
                headers = {
                    'Authorization': f'Bearer {owner_github_token}',
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28'
                }
                response = await client.get(
                    url,
                    headers=headers
                )

                response_data = response.json()
                
                commit_data = {
                    'sha': response_data['sha'],
                    'commit_message': response_data.get('commit').get('message'),
                    'commit_author_name': response_data.get('commit').get('author').get('name'),
                    'commit_created': response_data.get('commit').get('author').get('date'),
                    'additions': response_data.get('stats').get('additions'),
                    'deletions': response_data.get('stats').get('deletions'),
                    'files': response_data.get('files')
                }
                
                res.append(commit_data)
        return res
    
    
    async def verify_webhook_request(
        self,
        signature: str | None,
        project_webhook_secret: str,
        body: bytes
    ):
        if not signature:
            raise GithubApiException(401)
        
        expected = 'sha256=' + hmac.new(
            project_webhook_secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected, signature):
            raise GithubUnAutharize()
        print('Verified')
        return True
    
    async def handle_push(self, data: dict):
        commits_raw = data['commits']
        repo_full_name = data['repo_full_name']
        owner_github_token = data['owner_github_token']
        
        commits = await self.get_commits_from_webhook(commits_raw, repo_full_name, owner_github_token)
        print(commits)

        for commit in commits:
            answer = await self.ai_service.summarize_commit(commit)
            
            if not answer:
                raise Exception # TODO: exc

            answer = json.loads(answer)
            
            commit_data = CommitCreateSchema(
                commit_info=str(commit),
                project_id=data['project_id'],
                sha=answer['sha'],
                summary=answer['summary'],
                technical=answer['technical'],
                process=answer['process'],
                risks=answer['risks'],
                conventional_commits=answer['conventional_commits'],
                author=answer['author']
            )
            
            await self.commit_repo.create_commit(commit_data)
            
            return {'status': 'ok'}
            
            
        