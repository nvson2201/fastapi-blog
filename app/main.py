from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from app.api.api_v1.api import api_router
from . import crud, models, schemas
from app.core.config import settings

app = FastAPI()


app.include_router(api_router, prefix=settings.API_V1_STR)
