
from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login, users, comments, google, profiles
)
from app.api.api_v1.endpoints.posts import api as posts

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, tags=["posts"])
api_router.include_router(
    comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(google.router, tags=["google"])
api_router.include_router(
    profiles.router, prefix="/profiles", tags=["profiles"]
)
