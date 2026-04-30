from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.projects.models import Project
from src.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_project(self, project_data: ProjectCreateSchema) -> Project:
        pass
        
    async def get_project_by_id(self, id: int) -> Project:
        pass
        
    async def get_all_project_by_user(self, user_id: int) -> List[Project]:
        pass
        
    async def update_project(self, project_id: int, update_project: ProjectUpdateSchema) -> Project:
        pass
        
    async def delete_project(self, project_id: int) -> Project:
        pass