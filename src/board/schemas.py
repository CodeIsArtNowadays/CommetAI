from datetime import datetime

from pydantic import BaseModel, Field

from src.auth.schemas import UserInfoSchema


class ProjectBaseSchema(BaseModel):
    
    title: str
    description: str | None = Field(default=None)
    
    
class ProjectUpdateSchema(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    
    
class ProjectCreateRequestSchema(ProjectBaseSchema):
    pass


class ProjectCreateSchema(ProjectCreateRequestSchema):
    owner_id: int
    

class WebhookCreateSchema(BaseModel):
    repo_full_name: str
    owner_github_token: str

class WebhookDataCreateSchema(BaseModel):
    repo_full_name: str
    webhook_id: int
    webhook_secret: str

class ProjectRetrieveSchema(ProjectBaseSchema):
    id: int
    owner: UserInfoSchema
    created_at: datetime

class ProjectNestedRetrieveSchema(BaseModel):
    id: int
    title: str


class TaskBaseSchema(BaseModel):
    title: str
    due_time: datetime | None = Field(default=None)
    description: str | None = Field(default=None)
    is_done: bool = Field(default=False)
    
    
class TaskRetrieveSchema(TaskBaseSchema):
    id: int
    
    assignee: UserInfoSchema
    project: ProjectNestedRetrieveSchema


class TaskCreateSchema(TaskBaseSchema):
    project_id: int
    commit_sha: str
    

class TaskUpdateSchema(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_done: bool | None = Field(default=None)
    assignee_id: int | None = Field(default=None)
    due_time: datetime | None = Field(default=None)
    
    
class CommitCreateSchema(BaseModel):
    sha: str
    commit_info: str
    summary: str
    technical: str
    process: str
    risks: str
    project_id: int
    conventional_commits: bool
    author: str