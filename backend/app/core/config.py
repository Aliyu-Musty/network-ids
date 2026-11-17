from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time Network Attack Detection System"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/network_ids"
    SYNC_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/network_ids"
    JWT_SECRET: str = "supersecretkey_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    SNIFFER_INTERFACE: Optional[str] = None
    ALERT_CONFIDENCE_THRESHOLD: float = 0.70

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
