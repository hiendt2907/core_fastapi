# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    JWT_SECRET: str
    DATABASE_URL: str
    APP_ENV: str = "dev"  # thêm biến này, mặc định là dev

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

