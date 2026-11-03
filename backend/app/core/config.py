from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Securebox"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "change-me-in-production"
    DATABASE_URL: str = "sqlite+aiosqlite:///./securebox.db"
    
    # AI Configuration
    OPENAI_API_KEY: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
