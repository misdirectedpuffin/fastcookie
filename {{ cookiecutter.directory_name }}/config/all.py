import secrets
from os import getcwd
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, BaseSettings, EmailStr, PostgresDsn, validator


class Api(BaseModel):
    HOST: str = "api"
    INTERFACE: str = "0.0.0.0"
    DOMAIN: str = "api"
    PORT: int = 8888
    SCHEME: str = "http"
    V1_STR: str = "/api/v1"
    CORS_ORIGINS: list[str] = [
        "http://0.0.0.0:8888/",
        "https://0.0.0.0:8888/",
        "http://0.0.0.0:3000/",
        "https://0.0.0.0:3000/",
    ]

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: Union[List[str], str]) -> Union[List[str], str]:
        # sourcery skip: instance-method-first-arg-name
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)



class Smtp(BaseModel):
    TLS: bool = True
    PORT: Optional[int] = None
    HOST: Optional[str] = None
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None


# pylint: disable=no-self-argument
class Settings(BaseSettings):
    HTTP_REQ_TIMEOUT: int = 30
    PROJECT_NAME: str = '{{cookiecutter.database_container_name}}'
    API: Api = Api()
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENV: Literal["development", "test"] = "development"
    # 60 minutes * 24 hours * 8 days = 8 days

    SQLALCHEMY_DATABASE_URI: str = "postgresql+asyncpg://{{cookiecutter.database_container_name}}:{{cookiecutter.database_container_name}}@{{cookiecutter.database_container_name}}:5432/{{cookiecutter.database_container_name}}"
    SQLALCHEMY_SYNC_DATABASE_URI: str = "postgresql+psycopg2://{{cookiecutter.database_container_name}}:{{cookiecutter.database_container_name}}@{{cookiecutter.database_container_name}}:5432/{{cookiecutter.database_container_name}}"


    @validator("SQLALCHEMY_DATABASE_URI", pre=True, check_fields=True)
    def assemble_db_connection(cls, value: Optional[PostgresDsn], values: Dict[str, Any]) -> str:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER", "{{cookiecutter.database_container_name}}"),
            password=values.get("POSTGRES_PASSWORD", "{{cookiecutter.database_container_name}}"),
            host=values.get("POSTGRES_HOST", "{{cookiecutter.database_container_name}}"),
            port=values.get("POSTGRES_PORT", "5432"),
        )

    FIRST_SUPERUSER: EmailStr = "{{cookiecutter.superuser_email}}"  # type: ignore
    FIRST_SUPERUSER_PASSWORD: str = "{{cookiecutter.superuser_password}}"
    USERS_OPEN_REGISTRATION: bool = False
    LOG_LEVEL: str = "DEBUG"
    BASE_PATH: str = getcwd()
    class Config:
        case_sensitive = True
        env_file = "env/.development"
        env_nested_delimiter = "__"
