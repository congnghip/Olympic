import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DX-OS Open-Core Construction Platform"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "dxos_open_core_super_secret_key_change_in_production_2026"
    
    # DATABASE
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://dxos_admin:dxos_secret_password_2026@localhost:5432/dxos_construction"
    )
    
    # MINIO
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin_secret_2026")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "construction-dossiers")
    MINIO_SECURE: bool = False
    
    # FLOWABLE
    FLOWABLE_API_URL: str = os.getenv("FLOWABLE_API_URL", "http://localhost:8090/flowable-rest/service")
    FLOWABLE_ADMIN_USER: str = os.getenv("FLOWABLE_ADMIN_USER", "admin")
    FLOWABLE_ADMIN_PASSWORD: str = os.getenv("FLOWABLE_ADMIN_PASSWORD", "test")
    
    # AI SETTINGS
    USE_MOCK_AI: bool = True
    MOCK_LATENCY_SECONDS: float = 1.0

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
