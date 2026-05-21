from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.dependencies import get_ai_service
from src.ai.service import AiService
from src.board.repository import CommitRepository, ProjectRepository
from src.board.service import ProjectService, WebhookService
from src.core.database import get_db

async def get_commit_repo(session: AsyncSession = Depends(get_db)):
    return CommitRepository(session)


async def get_webhook_service(
    ai_service: AiService = Depends(get_ai_service),
    commit_repo: CommitRepository = Depends(get_commit_repo),
) -> WebhookService:
    return WebhookService(ai_service, commit_repo)





async def get_project_service(
    session: AsyncSession = Depends(get_db),
    webhook_service: WebhookService = Depends(get_webhook_service),
) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(repo, webhook_service)
