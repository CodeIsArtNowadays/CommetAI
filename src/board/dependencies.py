from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.service import AiService
from src.core.database import get_db
from src.ai.dependencies import get_ai_service
from src.board.repository import ProjectRepository
from src.board.service import ProjectService, WebhookService


async def get_webhook_service(ai_service: AiService = Depends(get_ai_service)) -> WebhookService:
    return WebhookService(ai_service)


async def get_project_service(
    session: AsyncSession = Depends(get_db),
    webhook_service: WebhookService = Depends(get_webhook_service)
) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(repo, webhook_service)
    
