from fastapi import APIRouter

from app.api.api_v1.endpoints.users import login, register, users_resource

router = APIRouter()

router.include_router(login.router, tags=["login"])
router.include_router(register.router, tags=["register"])
router.include_router(users_resource.router, tags=["users"], prefix="/users")
