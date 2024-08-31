from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLDB_URL: str
    SECRET_KEY: str = "secret"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5 * 60  # 5 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    model_config = SettingsConfigDict(
        env_file=".env", validate_assignment=True, extra="allow"
    )

"""

create file .env in the same level as moodtracker folder

in file .env
SQLDB_URL=postgresql+asyncpg://postgres:<your_password>@localhost:5432/your_database_name

"""

def get_settings():
    return Settings()