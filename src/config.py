from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    # 1NCE API
    ONENCE_USERNAME: str
    ONENCE_PASSWORD: str
    ONENCE_API_BASE_URL: str = "https://api.1nce.com/management-api"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Application
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-me-in-production"

    # Data Collection
    DATA_COLLECTION_INTERVAL_MINUTES: int = 60
    USAGE_RETENTION_DAYS: int = 180

    # Alerts
    ENABLE_EMAIL_ALERTS: bool = False
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    ALERT_EMAIL_TO: Optional[str] = None

    def validate(self):
        """Validate required settings"""
        if not self.ONENCE_USERNAME or not self.ONENCE_PASSWORD:
            raise ValueError("1NCE credentials not configured")
        return self


# Global config instance
config = Settings().validate()
