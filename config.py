from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = ''
    DB_PORT: str = ''
    DB_NAME: str = ''
    DB_USER: str = ''
    DB_PASS: str = ''
    
    
    model_config = SettingsConfigDict(env_file='.env')
    
    def get_async_db_dns(self) -> str:
        user = quote_plus(self.DB_USER)
        pswd = quote_plus(self.DB_PASS)
        
        return f'postgresql+asyncpg://{user}:{pswd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
settings = Settings()