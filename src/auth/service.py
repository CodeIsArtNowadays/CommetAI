from pwdlib import PasswordHash

from src.auth.repository import UserRepository
from src.auth.schemas import UserCredentialSchema
from src.auth.exceptions import NoUsernameMatchError
from src.auth.models import User


class UserService: 
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.password_hash = PasswordHash.recommended()
    
    async def create_user(self, user_data: UserCredentialSchema) -> User:
        hashed_pswd = await self.hash_password(user_data.password)
        user_data.password = hashed_pswd
        return await self.repo.create_user(user_data)
        
    async def login(self, user_data: UserCredentialSchema) -> bool:
        user = await self.repo.get_user_by_username(user_data.username)
        if not user:
            raise NoUsernameMatchError('No user with that username')
        
        
        return self.password_hash.verify(user_data.password, user.password)
    
    async def hash_password(self, s) -> str:
        return self.password_hash.hash(s)
        