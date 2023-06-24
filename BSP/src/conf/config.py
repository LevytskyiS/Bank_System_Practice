from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "db_connect"
    secret_key_jwt: str = "key"
    algorithm: str = "algo"

    mail_username: str = "mail"
    mail_password: str = "pass"
    mail_from: str = "hi"
    mail_port: int = 123
    mail_server: str = "post"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
