
from fastapi import FastAPI, Depends
from app.api.api_v1.api import api_router
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(SessionMiddleware, secret_key="!secret")
