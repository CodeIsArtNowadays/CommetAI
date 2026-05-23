import httpx
import json

from fastapi import Depends

from src.ai.dependencies import get_ai_service
from src.ai.service import AiService
from src.board.dependencies import get_commit_repo, get_project_service, get_task_repo
from src.board.project_service import ProjectService
from src.board.repository import CommitRepository, TaskRepository
from src.board.schemas import CommitCreateSchema, TaskCreateSchema



class ProcessPushUseCase:
    def __init__(
        self,
        commit_repo: CommitRepository = Depends(get_commit_repo),
        task_repo: TaskRepository = Depends(get_task_repo),
        ai_service: AiService = Depends(get_ai_service),
        project_service: ProjectService = Depends(get_project_service),
    ):
        self.commit_repo = commit_repo
        self.task_repo = task_repo
        self.ai_service = ai_service
        self.project_service = project_service

    async def _get_commits_full_info(
        self, commits: list, repo_full_name: str, owner_github_token: str
    ):

        commits_meta = []
        headers = {
            "Authorization": f"Bearer {owner_github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        async with httpx.AsyncClient() as client:
            for commit in commits:
                commit_id = commit["id"]
                url = (
                    f"https://api.github.com/repos/{repo_full_name}/commits/{commit_id}"
                )

                response = await client.get(url, headers=headers)
                # if not response.status_code == 201:
                #     raise Exception  # TODO: exc

                response = response.json()
                commit_data = response.get("commit")
                if not commit_data:
                    raise Exception  # TODO: exc
                
                commit_data = {
                    "sha": response["sha"],
                    "commit_message": commit_data.get("message"),
                    "commit_author_name": commit_data.get("author").get("name"),
                    "commit_created": commit_data.get("author").get("date"),
                    'diffs': {
                        "additions": response.get("stats").get("additions"),
                        "deletions": response.get("stats").get("deletions"),
                        "files": response.get("files"),
                    }
                }

                commits_meta.append(commit_data)

        return commits_meta
    
    async def _get_undone_tasks_titles_by_project_id(self, project_id: int):
        tasks = await self.task_repo.get_all_project_undone_tasks(project_id)
        return [task.title for task in tasks]
    
    async def _create_project_description(self, commits: list, project_id: int):
        project = await self.project_service.get_project(project_id)
        answer = await self.ai_service.create_project_description(commits, project.title)
        print('asdasdasd', answer['description'])
        project = await self.project_service.repo.set_project_description(project, answer['description'])
        
    
    async def __call__(self, data: dict):
        print('USE CASE START')
        commits = data["commits"]
        repo_full_name = data["repo_full_name"]
        owner_github_token = data["owner_github_token"]
        project_id = data['project_id']

        commits_meta = await self._get_commits_full_info(
            commits, repo_full_name, owner_github_token
        )
        existing_tasks = await self._get_undone_tasks_titles_by_project_id(project_id) 

        for commit in commits_meta:
            ai_data = {'commit_message': commit['commit_message'], 'diffs': commit['diffs']}
            ai_response = json.loads(await self.ai_service.summarize_commit(json.dumps(ai_data)))
            
            commit_create_data = CommitCreateSchema(
                commit_info=json.dumps(commit),
                project_id=project_id,
                sha=commit["sha"],
                summary=ai_response["summary"],
                technical=ai_response["technical"],
                process=ai_response["process"],
                risks=ai_response["risks"],
                conventional_commits=ai_response["conventional_commits"],
                author=commit["commit_author_name"],
            )
            
            await self.commit_repo.create(commit_create_data)
            
            new_task = await self.ai_service.create_task(commit_create_data.summary, existing_tasks)
            
            new_task['project_id'] = project_id
            new_task['commit_sha'] = commit['sha']
            
            
            new_task_schema = TaskCreateSchema(**new_task)

            task = await self.task_repo.create(new_task_schema)
            existing_tasks.append(task.title)
        
        project_commits = list(await self.commit_repo.get_commits_for_project(project_id))
        if len(project_commits) > 5:
            await self._create_project_description(project_commits, project_id)
        print('USE CASE END')
        return {'ok': True}
            