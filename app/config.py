import secrets
import datetime

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EXPEIRATION_TIME_CACHE: int = 60 * 24 * 5

    REDIS_PREFIX_USER = "user_id"
    REDIS_PREFIX_POST = "post_id"
    REDIS_PREFIX_COMMENT = "comment_id"
    REDIS_PREFIX_POST_VIEWS = "post_views"

    EMAILS_ENABLED: bool = False
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "nguyenvanson@gapo.com.vn"
    FIRST_SUPERUSER_USERNAME = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "string11A"
    USERS_OPEN_REGISTRATION: bool = False

    DATABASE_URL = "mysql+mysqlconnector://test:test@localhost:3306/fastapi_blog"  # noqa
    GOOGLE_CLIENT_ID = "1041701496632-i22nqlha32dsjlasvhlk0spaj7k10cil.apps.googleusercontent.com"  # noqa
    GOOGLE_CLIENT_SECRET = "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"
    REDIS_HOST = "localhost"
    REDIS_PASSWORD = "123456"

    KAFKA_PRODUCER_BOOTSTRAP_URL = 'localhost:29092'
    KAFKA_CONSUMER_BOOTSTRAP_URL = 'localhost:29092'
    KAFKA_ADMIN_BOOTSTRAP_URL = 'localhost:29092'
    KAFKA_TOPIC_POST_VIEWS = 'views'
    KAFKA_CONSUMER_GROUP = 'mygroup'
    KAFKA_SESSION_TIMEOUT_MS = 6000

    KAFKA_CONSUMER_CONFIG = {
        'bootstrap.servers': KAFKA_CONSUMER_BOOTSTRAP_URL,
        'group.id': KAFKA_CONSUMER_GROUP,
        'session.timeout.ms': KAFKA_SESSION_TIMEOUT_MS,
        'auto.offset.reset': 'earliest'
    }

    KAFKA_PRODUCER_CONFIG = {
        'bootstrap.servers': KAFKA_PRODUCER_BOOTSTRAP_URL
    }

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    def past_week(self):
        return datetime.datetime.utcnow() - datetime.timedelta(weeks=1)

    def current_time(self):
        return (datetime.datetime.utcnow() +
                datetime.timedelta(hours=7))
    # year 1 month 1 day 1
    START_TIME_DEFAULT = datetime.datetime(1, 1, 1, 0, 0, 0, 0)

    class Config:
        case_sensitive = True


settings = Settings()
