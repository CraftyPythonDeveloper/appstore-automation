from pathlib import Path
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):

    WRK_DIR: Path = Path(__file__).resolve().parents[1]

    ONLINE_SIM_APIKEY: str
    NOPECHA_API_KEY: str

    OXYLABS_USERNAME: str
    OXYLABS_PASSWORD: str
    OXYLABS_IP: str = "pr.oxylabs.io"
    OXYLABS_PORT: int = 7777

    class Config:
        env_file = "config/.env"
        env_file_encoding = 'utf-8'


settings = AppConfig()
