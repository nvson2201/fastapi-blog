from fastapi import APIRouter

from app.api.api_v1.endpoints.posts import posts_common, posts_resource

router = APIRouter()

router.include_router(posts_common.router, prefix="/posts")
router.include_router(posts_resource.router, prefix="/posts")
