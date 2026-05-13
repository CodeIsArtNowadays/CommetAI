from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.board.models import Project, Task
from src.board.schemas import ProjectCreateSchema, ProjectUpdateSchema, TaskCreateSchema, TaskUpdateSchema


class ProjectRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_project(self, project_data: ProjectCreateSchema) -> Project:
        project = Project(**project_data.model_dump())
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project
        
    async def get_project_by_id(self, project_id: int) -> Project:
        stmt = select(Project).where(Project.id==project_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
        
    async def get_all_project_by_user(self, user_id: int) -> Sequence[Project]:
        stmt = select(Project).where(Project.owner_id==user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()
        
    async def update_project(self, project_id: int, updated_project: ProjectUpdateSchema) -> Project:
        project = await self.get_project_by_id(project_id)
        for k, v in updated_project.model_dump(exclude_unset=True).items():
            setattr(project, k, v)
        await self.session.refresh(project)
        return project
        
    async def delete_project(self, project_id: int) -> None:
        stmt = delete(Project).where(Project.id==project_id)
        await self.session.execute(stmt)
        
        
class TaskRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_task(self, task_data: TaskCreateSchema) -> Task:
        task = Task(**task_data.model_dump())
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task
        
    async def update_task(self, task_id: int, updated_task: TaskUpdateSchema) -> Task:
        task = await self.get_task_by_id(task_id)
        for k, v in updated_task.model_dump(exclude_unset=True).items():
            setattr(task, k, v)
        await self.session.refresh(task)
        return task
        
    async def get_all_assingee_tasks(self, user_id: int) -> Sequence[Task]:
        stmt = select(Task).where(Task.assignee_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()
        
    async def get_task_by_id(self, task_id: int) -> Task:
        stmt = select(Task).where(Task.id == task_id)
        res = await self.session.execute(stmt)
        return res.scalar()
        
    async def delete_task(self, task_id: int) -> None:
        stmt = delete(Task).where(Task.id==task_id)
        await self.session.execute(stmt)
        
    