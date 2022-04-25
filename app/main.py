
from fastapi import FastAPI, Depends
from app.api.api_v1.api import api_router
from app.core.config import settings


from starlette.middleware.sessions import SessionMiddleware
from dependency_injector.wiring import inject, Provide
from app.redis.services import Service
from app.redis.containers import Container

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(SessionMiddleware, secret_key="!secret")


@app.get("/")
@inject
async def index(service: Service = Depends(Provide[Container.service])):
    value = await service.process()
    return {"result": value}


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost:6379")
container.config.redis_password.from_env("REDIS_PASSWORD", "123456")
container.wire(modules=[__name__])

app.include_router(api_router, prefix=settings.API_V1_STR)
