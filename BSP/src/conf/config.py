from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "db_connect"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
