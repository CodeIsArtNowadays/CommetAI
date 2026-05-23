from typing import Generic, Sequence, TypeVar

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.board.models import Project, Task, Commit
from src.board.schemas import WebhookDataCreateSchema


ModelType = TypeVar('ModelType')

class BaseRepository(Generic[ModelType]):
    
    model: type[ModelType]
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, id: int):
        res = await self.session.get(self.model, id)
        return res
    
    async def create(self, data):
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
        
    async def update(self, obj_id, upd_data):
        obj = await self.get_by_id(obj_id)
        for k, v in upd_data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
        
    async def delete(self, obj_id):
        obj = self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
    
class ProjectRepository(BaseRepository[Project]):

    model = Project

    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_all_project_by_user(self, user_id: int) -> Sequence[Project]:
        stmt = select(Project).where(Project.owner_id==user_id)
        res = await self.session.scalars(stmt)
        return res.all()
        
    async def set_wh_data(self, project: Project, wh_data: WebhookDataCreateSchema) -> Project:
        for k, v in wh_data.model_dump().items():
            setattr(project, k, v)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def get_project_by_repo_full_name(self, repo_full_name: str) -> Project:
        stmt = select(Project).where(Project.repo_full_name == repo_full_name)
        res = await self.session.scalar(stmt)
        return res
    
    async def set_project_description(self, project: Project, description: str) -> Project:
        project.description = description
        await self.session.flush()
        await self.session.refresh(project)
        return project
        
class TaskRepository(BaseRepository[Task]):
    
    model = Task
    
    async def get_all_project_undone_tasks(self, project_id: int) -> Sequence[Task]:
        stmt = select(Task).where(Task.project_id == project_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def done_task(self, task_id: int) -> Task:
        task = await self.get_by_id(task_id)
        if not task:
            raise Exception  # TODO: RepoExc(self.model, 404)
        task.is_done = True
        await self.session.flush()
        await self.session.refresh(task)
        return task
        
class CommitRepository(BaseRepository[Commit]):
    
    model = Commit
    
    async def get_project_commits_count(self, project_id):
        stmt = select(func.count()).select_from(self.model).where(self.model.project_id == project_id)
        res = await self.session.scalar(stmt)
        return res
        
    async def get_commits_for_project(self, project_id: int):
        stmt = select(self.model.summary).where(self.model.project_id == project_id)
        res = await self.session.scalars(stmt)
        return res.all()