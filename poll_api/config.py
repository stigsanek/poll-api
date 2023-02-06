import secrets
from typing import Any, List

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Project settings
    """
    API_V1: str = '/api/v1'
    PROJECT_NAME: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = True
    DATABASE_URL: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Parse values

            Args:
                field_name (str): Field name
                raw_val (str): Raw value

            Returns:
                Any: Converted value
            """
            if field_name == 'BACKEND_CORS_ORIGINS':
                return raw_val.split(',')
            return cls.json_loads(raw_val)


settings = Settings()
