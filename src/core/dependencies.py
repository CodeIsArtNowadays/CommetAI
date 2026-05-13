from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.dependencies import get_user_service
from src.auth.service import UserService
from src.auth.models import User


# class PaginationParams:
#     def __init__(
#         self, 
#         page: int = Query(default=1, ge=1),
#         size: int = Query(default=10, ge=5, le=100)
#     ):
#         self.page = page
#         self.size = size
        
#     def offset(self):
#         return (self.page - 1) * self.size
    

bearer = HTTPBearer()
    

async def get_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    user_service: UserService = Depends(get_user_service)
) -> User:
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No auth')
        
    token = creds.credentials
    decoded = await user_service.decode_jwt_token(token)
    
    if not decoded:
        raise 
        
    user_id = int(decoded['sub'])
    
    return await user_service.repo.get_user_by_id(user_id)
    
    
    