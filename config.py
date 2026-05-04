from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = ''
    DB_PORT: int = 0
    DB_NAME: str = ''
    DB_USER: str = ''
    DB_PASS: str = ''
    
    
    model_config = SettingsConfigDict(env_file='.env')
    
    @property
    def async_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    

@lru_cache
def get_settings():
    return Settings()
    
settings = get_settings()