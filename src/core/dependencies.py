from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.core.database import get_db
from src.projects.repository import ProjectRepository
from src.projects.service import ProjectService


class PaginationParams:
    def __init__(
        self, 
        page: int = Query(default=1, ge=1),
        size: int = Query(default=10, ge=5, le=100)
    ):
        self.page = page
        self.size = size
        
    def offset(self):
        return (self.page - 1) * self.size


def get_mock_user(x: int = 1) -> User:

    mocked_users = {
        1: User(id=1, username='MoonPie', password='test123'),
        2: User(id=2, username='Billie Jean King', password='test123')
    }

    return mocked_users[x]
    
    
async def get_project_service(session: AsyncSession = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(repo)