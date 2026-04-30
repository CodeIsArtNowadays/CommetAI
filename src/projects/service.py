from src.projects.repository import ProjectRepository
from src.projects.schemas import ProjectCreateRequestSchema, ProjectCreateSchema, ProjectUpdateSchema
from src.projects.models import Project
from src.core.database import get_db


class ProjectService():
        
    def __init__(self, repo: ProjectRepository):
        self.repo = repo
    
    async def create_project(self, project_schema: ProjectCreateRequestSchema, user_id: int) -> Project:
        pass
    
    async def _is_user_has_access_to_project(self, project_id: int, user_id: int) -> bool:
        pass
    
    async def get_project_by_id(self, id: int, user_id: int) -> Project:
        pass
        
    async def get_all_project_by_user(self, user_id: int) -> list[Project]:
        pass
        
    async def update_project(self, project_id: int, update_project: ProjectUpdateSchema, user_id: int) -> Project:
        pass
    
    async def delete_project(self, project_id: int, user_id: int) -> None:
        pass
        