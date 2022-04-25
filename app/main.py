from fastapi import FastAPI, Depends
from app.api.api_v1.api import api_router
from app.core.config import settings
import os


import json

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from dependency_injector.wiring import inject, Provide
from app.redis.services import Service
from app.redis.containers import Container

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="!secret")


# @app.get('/')
# async def home(request: Request):
#     user = request.session.get('user')
#     if user is not None:
#         email = user['email']
#         html = (
#             f'<pre>Email: {email}</pre><br>'
#             '<a href="/docs">documentation</a><br>'
#             '<a href="/logout">logout</a>'
#         )
#         return HTMLResponse(html)
#     return HTMLResponse('<a href="/login">login</a>')

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# Tag it as "authentication" for our docs
@app.get('/login', tags=['authentication'])
async def login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth')

    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    # Save the user
    request.session['user'] = dict(user)
    print(token)
    return RedirectResponse(url='/')


# Tag it as "authentication" for our docs
@app.get('/logout', tags=['authentication'])
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')


@app.api_route("/")
@inject
async def index(service: Service = Depends(Provide[Container.service])):
    value = await service.process()
    return {"result": value}


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost:6379")
container.config.redis_password.from_env("REDIS_PASSWORD", "123456")
container.wire(modules=[__name__])

app.include_router(api_router, prefix=settings.API_V1_STR)
