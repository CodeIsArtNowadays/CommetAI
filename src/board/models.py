from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.auth.models import User


class Project(Base):
    __tablename__ = 'projects'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(63))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
    repo_full_name: Mapped[str] = mapped_column(nullable=True, index=True, unique=True)
    webhook_id: Mapped[int] = mapped_column(nullable=True, unique=True, index=True)
    webhook_secret: Mapped[str] = mapped_column(nullable=True, unique=True)
    
    owner: Mapped[User] = relationship('User', lazy='joined')
    tasks: Mapped[list['Task']] = relationship('Task', back_populates='project', lazy='noload')
    commits: Mapped[list['Commit']] = relationship('Commit', back_populates='project', lazy='noload')
    
    
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    commit_sha: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    due_time: Mapped[datetime] = mapped_column(nullable=True)
    is_done: Mapped[bool] = mapped_column(default=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))

    project: Mapped[Project] = relationship(Project)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    

class Commit(Base):
    __tablename__ = 'commits'
    
    sha: Mapped[str] = mapped_column(primary_key=True, unique=True)
    commit_info: Mapped[str] = mapped_column(Text())
    summary: Mapped[str] = mapped_column()
    technical: Mapped[str] = mapped_column()
    process: Mapped[str] = mapped_column()
    risks: Mapped[str] = mapped_column()
    conventional_commits: Mapped[bool] = mapped_column()
    author: Mapped[str] = mapped_column()
    
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    
    project: Mapped[Project] = relationship(Project)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    def __str__(self):
        return self.summary
