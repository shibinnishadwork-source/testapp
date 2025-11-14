import os
from pydantic_settings import BaseSettings  

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY", "secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    gemini_api_key: str = os.getenv("gemini_api_key", "make a gemini_api_key")
settings = Settings()
