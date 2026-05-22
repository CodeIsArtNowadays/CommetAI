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

    async def _get_diffs_from_commits(
        self, commits: list, repo_full_name: str, owner_github_token: str
    ):

        diffs = []
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

                diff_data = {
                    "sha": response["sha"],
                    "commit_message": commit_data.get("message"),
                    "commit_author_name": commit_data.get("author").get("name"),
                    "commit_created": commit_data.get("author").get("date"),
                    "additions": response.get("stats").get("additions"),
                    "deletions": response.get("stats").get("deletions"),
                    "files": response.get("files"),
                }

                diffs.append(diff_data)

        return diffs
    
    async def _get_undone_tasks_by_project_id(self, project_id: int):
        return await self.task_repo.get_all_project_undone_tasks(project_id)
        
    
    async def __call__(self, data: dict):

        commits = data["commits"]
        repo_full_name = data["repo_full_name"]
        owner_github_token = data["owner_github_token"]

        diffs = await self._get_diffs_from_commits(
            commits, repo_full_name, owner_github_token
        )

        for diff in diffs:
            ai_response = json.loads(await self.ai_service.summarize_commit(diff))
            
            commit_data = CommitCreateSchema(
                commit_info=str(diff),
                project_id=data["project_id"],
                sha=diff["sha"],
                summary=ai_response["summary"],
                technical=ai_response["technical"],
                process=ai_response["process"],
                risks=ai_response["risks"],
                conventional_commits=ai_response["conventional_commits"],
                author=ai_response["author"],
            )
            
            await self.commit_repo.create(commit_data)
            
            existing_tasks = await self._get_undone_tasks_by_project_id(data['project_id'])
            print(existing_tasks)
            
            new_task = await self.ai_service.create_task(commit_data.summary, existing_tasks)
            
            new_task_schema = TaskCreateSchema(**new_task)

            await self.task_repo.create(new_task_schema)