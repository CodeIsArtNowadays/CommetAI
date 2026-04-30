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