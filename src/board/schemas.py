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
    
    
class ProjectRetrieveSchema(ProjectBaseSchema):
    id: int
    owner: UserInfoSchema
    created_at: datetime

class ProjectNestedRetrieveSchema(BaseModel):
    id: int
    title: str


class TaskBaseSchema(BaseModel):
    title: str
    due_time: datetime
    is_done: bool = Field(default=False)
    
    
class TaskRetrieveSchema(TaskBaseSchema):
    id: int
    description: str | None = Field(default=None)
    assignee: UserInfoSchema
    project: ProjectNestedRetrieveSchema


class TaskCreateSchema(TaskBaseSchema):
    project_id: int
    assignee_id: int
    

class TaskUpdateSchema(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_done: bool | None = Field(default=None)
    assignee_id: int | None = Field(default=None)
    due_time: datetime | None = Field(default=None)
    
    