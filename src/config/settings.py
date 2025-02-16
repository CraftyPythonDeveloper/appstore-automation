from pathlib import Path
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):

    WRK_DIR: Path = Path(__file__).resolve().parents[1]

    ONLINE_SIM_APIKEY: str
    NOPECHA_API_KEY: str

    class Config:
        env_file = "config/.env"
        env_file_encoding = 'utf-8'


settings = AppConfig()
