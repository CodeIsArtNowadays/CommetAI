import secrets
from datetime import datetime, timedelta

import httpx
import jwt
from pwdlib import PasswordHash

from config import settings
from src.auth.models import User
from src.auth.repository import UserRepository
from src.auth.schemas import (
    UserCreateWithGithubSchema,
)


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.password_hash = PasswordHash.recommended()

    async def create_user(self, user_data: UserCreateWithGithubSchema) -> User:
        user = await self.repo.create_user(user_data)
        return user

    async def create_jwt_token(self, user_id: int) -> str:
        payload = {
            'user_id': user_id,
            'expire': str(datetime.now() + timedelta(days=7))
        }
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
    
    async def github_auth(self, code: str):
        github_user, access_token = await self.github_get_user_data_by_code(code)
        user = await self.repo.get_user_by_github_id(github_user['id'])
        
        if not user:
            user = await self.create_user(UserCreateWithGithubSchema(
                username=github_user['login'],
                github_id=github_user['id'],
                github_token=access_token
            ))
        
        return await self.create_jwt_token(user.id)
    
    async def github_get_user_data_by_code(self, code: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                params={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                },
                headers={"Accept": "application/json"},
            )

            if not response.status_code == 200:
                raise Exception # TODO: exc
            
            response_data = response.json()
            access_token = response_data.get("access_token")
            
            if not access_token:
                raise Exception  # TODO: exc

            user = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                },
            )
            return user.json(), access_token