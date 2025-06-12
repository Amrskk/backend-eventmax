from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    OPENROUTER_API_KEY: str
    SECRET_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
