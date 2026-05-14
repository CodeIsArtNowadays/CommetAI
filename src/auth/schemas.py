from pydantic import BaseModel, ConfigDict, Field


class BaseUserSchema(BaseModel):
    username: str = Field(max_length=31)
    
    model_config = ConfigDict(
        from_attributes=True
    )

class UserInfoSchema(BaseUserSchema):
    pass
    
class UserCreateResponse(BaseUserSchema):
    access_token: str
    refresh_token: str
    
class RefreshTokenCreateSchema(BaseModel):
    token: str
    jti: str
    user_id: int
        
class UserCreateWithGithubSchema(BaseUserSchema):
    github_id: int
    github_token: str
