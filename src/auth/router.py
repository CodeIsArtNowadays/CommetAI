from fastapi import APIRouter, Depends

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