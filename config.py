# config.py
from pydantic import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Stable Diffusion Music AI API"
    API_TOKEN: str
    MODEL_VERSION: str

    class Config:
        env_file = ".env"

settings = Settings()