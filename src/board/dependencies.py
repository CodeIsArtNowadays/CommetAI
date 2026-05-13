from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.board.repository import ProjectRepository
from src.board.service import ProjectService


async def get_project_service(session: AsyncSession = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(repo)