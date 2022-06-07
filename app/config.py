from functools import lru_cache
from typing import List, Literal, Union
from ipaddress import IPv4Address

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Project
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_NAME: str = "Test Task"
    PROJECT_IP: Union[IPv4Address, str] = "localhost"
    PROJECT_PORT: int = 8008
    ALLOWED_HOSTS: List[str] = ["*"]

    # Security
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    SECURITY_REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    SECURITY_SECRET_KEY: str = "ffuwefundomsdngjnjfqekrmi23jiojio5u4358u3fdgjgfh"
    SECURITY_ALGORITHM: Literal["HS256"] = "HS256"
    SECURITY_ACCESS_TOKEN_URL: str = "/login"
    SECURITY_REFRESH_TOKEN_COOKIE_KEY: str = "test_task_cookie"
    SECURITY_REFRESH_TOKEN_COOKIE_EXPIRES: int = 2592000  # seconds (30 days)
    SECURITY_REFRESH_TOKEN_URL: str = "/token/refresh"
    SECURITY_REFRESH_TOKEN_COOKIE_PATH: str = SECURITY_REFRESH_TOKEN_URL
    SECURITY_REFRESH_TOKEN_COOKIE_DOMAIN: str = "localhost"
    SECURITY_REFRESH_TOKEN_COOKIE_HTTPONLY: bool = True
    SECURITY_REFRESH_TOKEN_COOKIE_SECURE: bool = True
    SECURITY_REFRESH_TOKEN_COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "none"

    # Database
    # DB_USER: str = "tolikdemchuk"
    # DB_HOST: str = "localhost"
    # DB_PORT: int = 5432
    # DB_PASSWORD: str = ""
    # DB_NAME: str = "test_work"
    # SQLALCHEMY_DATABASE_URI: str = "postgresql://{}:{}@{}:{}/{}".format(
    #     DB_USER,
    #     DB_PASSWORD,
    #     DB_HOST,
    #     DB_PORT,
    #     DB_NAME
    # )

    SQLALCHEMY_DATABASE_URI: str = Field(..., env='DATABASE_URL')


@lru_cache()
def cached_settings():
    return Settings()


settings = cached_settings()
