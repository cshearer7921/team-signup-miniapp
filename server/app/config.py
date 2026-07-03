from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Team Signup Miniapp"
    env: str = "dev"
    api_prefix: str = "/api"

    database_url: str = "mysql+pymysql://team_signup:team_signup@mysql:3306/team_signup?charset=utf8mb4"
    redis_url: str = "redis://redis:6379/0"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 30

    wechat_appid: str = ""
    wechat_secret: str = ""
    wechat_mock_login: bool = True

    default_team_name: str = "业余足球队"
    admin_username: str = "admin"
    admin_password: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
