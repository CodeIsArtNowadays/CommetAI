from sqlalchemy.ext.asyncio import AsyncSession

from src.webhook.models import WebhookRecord
from src.webhook.schemas import WhRecordCreateSchema


class WebhookRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_webhook_record(self, webhook_record_data: WhRecordCreateSchema):
        
        wh_record = WebhookRecord(**webhook_record_data.model_dump())
        self.session.add(wh_record)
        await self.session.flush()
        await self.session.refresh(wh_record)
        
        return wh_record