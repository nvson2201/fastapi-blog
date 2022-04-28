import secrets

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EXPEIRATION_TIME_CACHE: int = 60 * 24 * 5

    REDIS_SUFFIX_USER = "user_id"
    REDIS_SUFFIX_POST = "post_id"
    REDIS_SUFFIX_COMMENT = "comment_id"

    EMAILS_ENABLED: bool = False
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "nguyenvanson@gapo.com.vn"
    FIRST_SUPERUSER_PASSWORD: str = "1234567"
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
