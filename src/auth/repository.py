from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserCredentialSchema, RefreshTokenCreateSchema
from src.auth.models import RefreshTokenModel, User as UserModel


class UserRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_user(self, user_data: UserCredentialSchema):
        user = UserModel(**user_data.model_dump())
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
        
    async def get_user_hashed_pass(self, user_id) -> str | None:
        stmt = select(UserModel.password).where(UserModel.id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.username == username)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id) -> UserModel | None:
        return await self.session.get(UserModel, user_id)
        
    async def create_refresh_token(self, ref_token_data: RefreshTokenCreateSchema) -> RefreshTokenModel:
        ref_token = RefreshTokenModel(**ref_token_data.model_dump())
        self.session.add(ref_token)
        await self.session.flush()
        await self.session.refresh(ref_token)
        return ref_token