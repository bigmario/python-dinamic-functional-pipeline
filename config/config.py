import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str

    class Config(BaseSettings.Config):
        env_file = ".env"
