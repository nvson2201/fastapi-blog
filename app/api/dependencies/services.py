from fastapi import Depends

from app.api.dependencies.repositories import get_redis_repo
from app.db.repositories.posts import PostRepository
from app.db.repositories.users import UserRepository
from app.db.repositories_cache.posts import PostRedisRepository
from app.db.repositories_cache.users import UserRedisRepository
from app.services.authentication import AuthenticationService
from app.services.login import LoginServices
from app.services.posts import PostServices
from app.services.profiles import ProfileServices
from app.services.users import UserServices


def get_user_services(
    user_redis_repo=Depends(get_redis_repo(
        UserRedisRepository, UserRepository))
):
    return UserServices(user_redis_repo)


def get_profile_services(
    user_redis_repo=Depends(get_redis_repo(
        UserRedisRepository, UserRepository))
):
    return ProfileServices(user_redis_repo)


def get_auth_services(
    user_redis_repo=Depends(get_redis_repo(
        UserRedisRepository, UserRepository))
):
    return AuthenticationService(user_redis_repo)


def get_login_services(
    user_redis_repo=Depends(get_redis_repo(
        UserRedisRepository, UserRepository)),
    user_services=Depends(get_user_services)
):
    return LoginServices(repository=user_redis_repo,
                         user_services=user_services)


def get_post_services(
    post_redis_repo=Depends(get_redis_repo(
        PostRedisRepository, PostRepository)),
    profile_services=Depends(get_profile_services)
):
    return PostServices(repository=post_redis_repo,
                        profile_services=profile_services)
