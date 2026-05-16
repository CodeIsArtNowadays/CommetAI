import uuid
import httpx

from src.auth.models import User
from src.board.models import Project
from src.board.repository import ProjectRepository
from src.board.schemas import (
    ProjectCreateRequestSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    WebhookDataCreateSchema,
)
from src.core.exceptions import (
    ProjectAccessIsNotAllowedException,
    ProjectNotFoundException,
)


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo
        self.base_url = "https://api.github.com"

    async def create_webhook(self, repo_full_name, owner_github_token: str):

        async with httpx.AsyncClient() as client:
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {owner_github_token}",
            }
            uri = self.base_url + f"/repos/{repo_full_name}/hooks"
            secret = str(uuid.uuid4())
            response = await client.post(
                uri,
                headers=headers,
                json={
                    "name": "web",
                    "active": True,
                    "events": ["push"],
                    "config": {
                        "url": "https://peddling-unsure-unpaid.ngrok-free.dev/webhook/event",
                        "content_type": "json",
                        "secret": secret,
                    },
                },
            )
            if not response.status_code == 201:
                raise Exception # TODO: exc
            response_data = response.json()
            return {
                'wh_id': response_data['id'],
                'secret': secret
            }
            
    async def create_project(
        self, project_schema: ProjectCreateRequestSchema, user: User
    ) -> Project:
        project_complete_schema = ProjectCreateSchema(
            **project_schema.model_dump(), owner_id=user.id
        )
        project = await self.repo.create_project(project_complete_schema)
        repo_full_name = project.owner.username + '/' + project.title
        
        wh_data_raw = await self.create_webhook(repo_full_name, user.github_token)
        
        wh_data = WebhookDataCreateSchema(
            webhook_id=wh_data_raw['wh_id'],
            webhook_secret=wh_data_raw['secret'],
            repo_full_name=repo_full_name
        )
        print('update')
        print(wh_data)
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
    
    def __init__(self):
        pass
        
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
                        'content': 'json'
                    }
                }
            )
            
            if not response.status_code == 201:
                raise Exception  # TODO: exc
                
            response_data = response.json()
            return {
                'wh_id': response_data['id'],
                'secret': secret
            }
    
    async def get_commits_from_webhook_callback(self):
        pass
    
    async def verify_webhook_request(self):
        pass
        