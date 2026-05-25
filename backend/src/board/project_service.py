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
from src.board.webhook_service import WebhookService


class ProjectService:
    def __init__(self, repo: ProjectRepository, webhook_service: WebhookService):
        self.repo = repo
        self.webhook_service = webhook_service

    async def create_project(
        self, project_schema: ProjectCreateRequestSchema, user: User
    ) -> Project:
        project_complete_schema = ProjectCreateSchema(
            **project_schema.model_dump(), owner_id=user.id
        )
        project = await self.repo.create(project_complete_schema)
        repo_full_name = project.owner.username + "/" + project.title

        try:
            wh_data_raw = await self.webhook_service.create_webhook(
                repo_full_name, user.github_token
            )
        except Exception:
            await self.repo.session.rollback()  # убираем мусорную запись
            raise

        wh_data = WebhookDataCreateSchema(
            webhook_id=wh_data_raw["wh_id"],
            webhook_secret=wh_data_raw["secret"],
            repo_full_name=repo_full_name,
        )

        project = await self.repo.set_wh_data(project, wh_data)

        return project

    async def _get_project_or_403(self, project_id: int, user_id: int) -> Project:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException()
        if not project.owner_id == user_id:
            raise ProjectAccessIsNotAllowedException()
        return project

    async def get_project_by_id(self, project_id: int, user_id: int) -> Project:
        return await self._get_project_or_403(project_id, user_id)
        
    async def get_project(self, project_id) -> Project:
        return await self.repo.get_by_id(project_id)

    async def get_all_project_by_user(self, user_id: int) -> list[Project]:
        res = await self.repo.get_all_project_by_user(user_id)
        return list(res)

    async def update_project(
        self, project_id: int, update_project: ProjectUpdateSchema, user_id: int
    ) -> Project:
        await self._get_project_or_403(project_id, user_id)
        return await self.repo.update(project_id, update_project)

    async def delete_project(self, project_id: int, user_id: int) -> None:
        await self._get_project_or_403(project_id, user_id)
        await self.repo.delete(project_id)
