import json
import httpx

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from config import settings
from src.auth.models import User
from src.auth.schemas import UserCredentialSchema, UserCreateResponse
from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.core.dependencies import get_user

auth_router = APIRouter()


@auth_router.get('/')
async def index(service: UserService = Depends(get_user_service)):
    return await service.repo.get_user_hashed_pass(1)
    
    
@auth_router.post('/signup', response_model=UserCreateResponse)
async def signup(user_data: UserCredentialSchema, service: UserService = Depends(get_user_service)):
    return await service.create_user(user_data)
    

@auth_router.post('/login')
async def login(user_data: UserCredentialSchema, service: UserService = Depends(get_user_service)):
    return await service.login(user_data)
    
@auth_router.get('/profile')
async def profile(user: User = Depends(get_user)):
    return user
    
@auth_router.get('/github')
async def github_redirect():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}"
    )
    
    
@auth_router.get('/callback/github')
async def github_callback(code: str):
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"}
        )
        
        response_data = response.json()
        access_token = response_data.get('access_token')
        print(access_token)
        
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )
        
        return user_response.json()