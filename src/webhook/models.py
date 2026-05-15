from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class WebhookRecord(Base):
    __tablename__ = 'webhooks_records'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    repo_id: Mapped[int] = mapped_column(ForeignKey('projects_id'), index=True, unique=True)
    webhook_id: Mapped[int] = mapped_column()
    secret: Mapped[str] = mapped_column(unique=True)