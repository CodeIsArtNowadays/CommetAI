from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.webhook.service import WebhookService
from src.webhook.repository import WebhookRepository


async def get_wh_repo(session: AsyncSession = Depends(get_db)):
    return WebhookRepository(session)

async def get_wh_service(repo: WebhookRepository = Depends(get_wh_repo)):
    return WebhookService(repo)