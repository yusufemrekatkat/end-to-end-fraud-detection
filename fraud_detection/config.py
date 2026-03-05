from enum import Enum
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    app_env: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
    model_version: str = "0.1.0"
    fraud_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    project_root: Path = Path(__file__).resolve().parent.parent
    data_raw_dir: Path = Path("data/raw")
    data_processed_dir: Path = Path("data/processed")
    models_dir: Path = Path("models")
    logs_dir: Path = Path("logs")
    random_seed: int = 42
    test_size: float = Field(default=0.2, gt=0.0, lt=1.0)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

def get_settings() -> Settings:
    return Settings()