from typing import List, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.projects.models import Project
from src.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_project(self, project_data: ProjectCreateSchema) -> Project:
        project = Project(**project_data.model_dump())
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project
        
    async def get_project_by_id(self, id: int) -> Project:
        stmt = select(Project).where(Project.id==id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
        
    async def get_all_project_by_user(self, user_id: int) -> Sequence[Project]:
        stmt = select(Project).where(Project.owner_id==user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()
        
    async def update_project(self, project_id: int, update_project: ProjectUpdateSchema) -> Project:
        pass
        
    async def delete_project(self, project_id: int) -> None:
        stmt = delete(Project).where(Project.id==id)
        await self.session.execute(stmt)
        