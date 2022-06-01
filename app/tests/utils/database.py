
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import settings


engine = create_engine(settings.DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
