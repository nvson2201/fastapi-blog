
from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    comments, google, profiles
)
from app.api.api_v1.endpoints.posts import api as posts
from app.api.api_v1.endpoints.users import api as users

api_router = APIRouter()
api_router.include_router(posts.router, tags=["posts"])
api_router.include_router(users.router)

api_router.include_router(
    comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(google.router, tags=["google"])
api_router.include_router(
    profiles.router, prefix="/profiles", tags=["profiles"]
)
