from src.core.dependencies import PaginationParams
from src.core.exceptions import ProjectNotFoundException, ProjectAccessIsNotAllowedException
from src.projects.repository import ProjectRepository
from src.projects.schemas import ProjectCreateRequestSchema, ProjectCreateSchema, ProjectUpdateSchema
from src.projects.models import Project

class ProjectService():
        
    def __init__(self, repo: ProjectRepository):
        self.repo = repo
    
    async def create_project(self, project_schema: ProjectCreateRequestSchema, user_id: int) -> Project:
        project_complete_schema = ProjectCreateSchema(**project_schema.model_dump(), owner_id=user_id)
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
        
    async def get_all_project_by_user(self, user_id: int, pagination: PaginationParams) -> list[Project]:
        res = await self.repo.get_all_project_by_user(user_id, pagination)
        return list(res)
        
    async def update_project(self, project_id: int, update_project: ProjectUpdateSchema, user_id: int) -> Project:
        await self._get_project_or_403(project_id, user_id)
        return await self.repo.update_project(project_id, update_project)
    
    async def delete_project(self, project_id: int, user_id: int) -> None:
        await self._get_project_or_403(project_id, user_id)
        await self.repo.delete_project(project_id)
        