from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.api.dependencies import authentication
from app.services.exceptions.favorites import (
    PostStillNotFavorited, PostAlreadyFavoried)
from app.services.posts import PostServices

router = APIRouter()


@router.post("/{id}/favorite", response_model=schemas.PostInResponse)
def mark_post_as_favorite(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends()
) -> schemas.PostInResponse:
    try:
        return post_services.mark_post_as_favorite(id=id, user=current_user)
    except PostAlreadyFavoried:
        raise HTTPException(
            status_code=400,
            detail="Already mark post as favorite!"
        )


@router.delete("/{id}/favorite", response_model=schemas.PostInResponse)
def remove_post_from_favorites(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends()
) -> schemas.PostInResponse:
    try:
        return post_services.remove_post_from_favorites(
            id=id, user=current_user
        )
    except PostStillNotFavorited:
        raise HTTPException(
            status_code=400,
            detail="This post has not been marked as favorite!"
        )


@router.get("/feed", response_model=schemas.ListOfPostsInResponse)
def get_posts_for_user_feed(
    limit: int = 20,
    offset: int = 0,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends()
) -> schemas.ListOfPostsInResponse:

    return post_services.get_posts_for_user_feed(
        user=current_user, limit=limit, offset=offset
    )
