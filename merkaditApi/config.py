from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    MYSQL_HOST: str = Field(default="localhost")
    MYSQL_PORT: int = Field(default=3306)
    MYSQL_USER: str = Field(default="usuario")
    MYSQL_PASSWORD: str = Field(default="password")
    MYSQL_DB: str = Field(default="merkadit_db")
    MYSQL_CHARSET: str = Field(default="utf8mb4")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

