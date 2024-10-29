from pydantic import BaseModel, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.db import DB

USERS_FOR_DB = [
    {
        "username": "jessika",
        "email": None,
        "number_upload_files": 27,
        "name_top_file": "encyclopedia.txt"
    },
    {
        "username": "john",
        "email": None,
        "number_upload_files": 805,
        "name_top_file": "encyclopedia.txt"
    },
    {
        "username": "alexander",
        "email": None,
        "number_upload_files": 2029,
        "name_top_file": "cats.jpeg"
    },
    {
        "username": "ben",
        "email": None,
        "number_upload_files": 72,
        "name_top_file": "cats.jpeg"
    },
    {
        "username": "julie",
        "email": None,
        "number_upload_files": 7828,
        "name_top_file": "all stars.jpeg"
    },
]


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="allow"
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig


settings = Settings()

db = DB(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
)
