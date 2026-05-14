import httpx

from src.auth.repository import UserRepository
from src.board.models import Project
from src.board.repository import ProjectRepository
from src.board.schemas import (
    ProjectCreateRequestSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from src.core.exceptions import (
    ProjectAccessIsNotAllowedException,
    ProjectNotFoundException,
)


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo
        self.base_url = "https://api.github.com"

    async def create_webhook(self, project_name, user_id):

        owner = await UserRepository(self.repo.session).get_user_by_id(user_id)
        if not owner:
            raise Exception

        async with httpx.AsyncClient() as client:
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {owner.github_token}",
            }
            uri = self.base_url + f"/repos/{owner.username}/{project_name}/hooks"
            print("check1")
            print(uri)
            response = await client.post(
                uri,
                headers=headers,
                json={
                    "name": "web",
                    "active": True,
                    "events": ["push"],
                    "config": {
                        "url": "https://peddling-unsure-unpaid.ngrok-free.dev/webhooks/github",
                        "content_type": "json",
                        "secret": "ahepfokgj1njbbh48j",
                    },
                },
            )

            print(response.status_code)
            

    async def create_project(
        self, project_schema: ProjectCreateRequestSchema, user_id: int
    ) -> Project:
        project_complete_schema = ProjectCreateSchema(
            **project_schema.model_dump(), owner_id=user_id
        )
        return await self.repo.create_project(project_complete_schema)

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
