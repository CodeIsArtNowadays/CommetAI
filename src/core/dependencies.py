from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.core.database import get_db
from src.projects.repository import ProjectRepository
from src.projects.service import ProjectService


def get_mock_user(x: int = 1) -> User:

    mocked_users = {
        1: User(id=1, username='MoonPie', password='test123'),
        2: User(id=2, username='Billie Jean King', password='test123')
    }

    return mocked_users[x]
    
    
async def get_project_service(session: AsyncSession = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(repo)