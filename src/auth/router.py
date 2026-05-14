from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from config import settings
from src.auth.models import User
from src.auth.service import UserService
from src.auth.dependencies import get_user_service
from src.core.dependencies import get_user

auth_router = APIRouter()

    
@auth_router.get('/profile')
async def profile(user: User = Depends(get_user)):
    return user
    
@auth_router.get('/github')
async def github_redirect():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}"
    )
    
@auth_router.get('/callback/github')
async def github_callback(code: str, service: UserService = Depends(get_user_service)):
    return await service.github_auth(code)
    
    