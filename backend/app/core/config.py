"""Application Configuration"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "ANH Smart Reporter"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 9110
    WORKERS: int = 4

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://anh_user:anh_password@postgres:5432/anh_reporter",
        description="PostgreSQL connection string"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = Field(
        default="redis://redis:6379/0",
        description="Redis connection string"
    )
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # Security
    SECRET_KEY: str = Field(
        default="change-this-to-a-secure-random-key-in-production",
        description="Secret key for JWT token generation"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:8080",
        "http://frontend:8080"
    ]

    # ANH Configuration
    ANH_FTP_HOST: str = Field(default="ftp.anh.gov.co", description="ANH FTP server")
    ANH_FTP_PORT: int = 21
    ANH_FTP_USER: str = Field(default="", description="ANH FTP username")
    ANH_FTP_PASSWORD: str = Field(default="", description="ANH FTP password")
    ANH_UPLOAD_TIME: str = "06:50"  # 6:50 AM COT
    ANH_REPORT_GENERATION_TIME: str = "06:00"  # 6:00 AM COT

    # Telemetry
    TELEMETRY_SAMPLE_INTERVAL: int = 600  # 10 minutes = 600 seconds (144 samples/day)
    TELEMETRY_BATCH_SIZE: int = 1000
    TELEMETRY_RETENTION_DAYS: int = 1825  # 5 years

    # OPC UA
    OPCUA_ENABLED: bool = True
    OPCUA_ENDPOINT: str = "opc.tcp://localhost:4840"
    OPCUA_NAMESPACE: int = 2

    # Modbus
    MODBUS_ENABLED: bool = True
    MODBUS_HOST: str = "localhost"
    MODBUS_PORT: int = 502

    # MQTT
    MQTT_ENABLED: bool = True
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC_PREFIX: str = "anh/telemetry"

    # Email Notifications
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "anh-reporter@insaingenieria.com"
    ALERT_EMAILS: List[str] = []

    # Machine Learning
    ML_ANOMALY_DETECTION: bool = True
    ML_MODEL_PATH: str = "/app/models"
    ML_RETRAIN_INTERVAL_HOURS: int = 24

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    METRICS_PORT: int = 9090

    # Data Quality
    MIN_DATA_QUALITY_SCORE: float = 95.0
    MAX_MISSING_SAMPLES: int = 10  # Out of 144 daily samples

    # Rust Engine
    RUST_ENGINE_ENABLED: bool = True
    RUST_ENGINE_URL: str = "http://rust-engine:8080"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
