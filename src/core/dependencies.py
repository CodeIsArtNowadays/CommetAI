from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import get_db
from src.auth.models import User
from src.board.repository import ProjectRepository
from src.board.service import ProjectService
from src.core.mock import get_mock_user


# class PaginationParams:
#     def __init__(
#         self, 
#         page: int = Query(default=1, ge=1),
#         size: int = Query(default=10, ge=5, le=100)
#     ):
#         self.page = page
#         self.size = size
        
#     def offset(self):
#         return (self.page - 1) * self.size

async def get_project_service(session: AsyncSession = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(repo)
    
    
async def get_user() -> User:
    return get_mock_user()