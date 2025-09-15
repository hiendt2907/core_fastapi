# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    JWT_SECRET: str
    DATABASE_URL: str
    APP_ENV: str = "dev"  # thêm biến này, mặc định là dev


settings = Settings()

