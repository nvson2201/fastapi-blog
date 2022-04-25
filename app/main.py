from app.redis.connect import Container
from fastapi import FastAPI, Depends
from app.api.api_v1.api import api_router
from app.core.config import settings


from starlette.middleware.sessions import SessionMiddleware
from dependency_injector.wiring import inject, Provide
from app.redis.services import Service


app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(SessionMiddleware, secret_key="!secret")


# Test Redis API
@app.api_route("/")
@inject
async def index(service: Service = Depends(Provide[Container.service])):
    value = await service.process()
    return {"result": value}
