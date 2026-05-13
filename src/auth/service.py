import secrets
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from config import settings
from src.auth.exceptions import NoUsernameMatchError
from src.auth.repository import UserRepository
from src.auth.schemas import RefreshTokenCreateSchema, UserCreateResponse, UserCredentialSchema


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.password_hash = PasswordHash.recommended()

    async def create_user(self, user_data: UserCredentialSchema) -> UserCreateResponse:
        hashed_pswd = await self.hash_password(user_data.password)
        user_data.password = hashed_pswd
        user = await self.repo.create_user(user_data)
        jwt_tokens = await self.login(user_data)
        return UserCreateResponse(
            **user,
            access_token=jwt_tokens["access_token"],
            refresh_token=jwt_tokens["refresh_token"],
        )

    async def login(self, user_data: UserCredentialSchema) -> dict:
        user = await self.repo.get_user_by_username(user_data.username)
        if not user:
            raise NoUsernameMatchError("No user with that username")
        if not self.password_hash.verify(user_data.password, user.password):
            raise NoUsernameMatchError("No user with that username")  # TODO: BadCredExc

        access_token = await self.create_jwt_token({"sub": str(user.id)})
        refresh_token = await self.generate_refresh_token()
        
        ref_token_data = RefreshTokenCreateSchema(
            user_id=user.id,
            token=refresh_token,
            jti=str(uuid4())
        )
        
        await self.repo.create_refresh_token(ref_token_data)
        
        return {'access_token': access_token, 'refresh_token': refresh_token}

    async def create_jwt_token(self, payload: dict) -> str:
        payload["expire"] = str(datetime.now() + timedelta(days=7))
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    async def generate_refresh_token(self):
        return secrets.token_urlsafe(32)

    async def decode_jwt_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def hash_password(self, s) -> str:
        return self.password_hash.hash(s)
