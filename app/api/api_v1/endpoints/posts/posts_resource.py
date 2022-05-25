from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.db import repositories
from app.api.dependencies import authentication
from app.services.exceptions.posts import PostNotFound
from app.services.posts import post_services
from app.api.dependencies.posts import get_post_filters
from app.schemas import PostsFilters, ListOfPostsInResponse

router = APIRouter()


@router.get("", response_model=ListOfPostsInResponse)
def read_posts(
    posts_filters: PostsFilters = Depends(get_post_filters),
    current_user: models.User = Depends(authentication.get_current_active_user)
) -> ListOfPostsInResponse:
    return post_services.posts_filters(
        tags=posts_filters.tags,
        author=posts_filters.author,
        user_favorited=posts_filters.user_favorited,
        limit=posts_filters.limit,
        offset=posts_filters.offset,
        requested_user=current_user,
    )


@router.post("/", response_model=schemas.PostInResponse)
def create_post(
    *,
    body: schemas.PostCreate,
    current_user: models.User = Depends(
        authentication.get_current_active_user)
) -> Any:
    """
    Create new post.
    """
    post = post_services.create_with_owner(
        body=body, author_id=current_user.id)
    return post


@router.put("/{id}", response_model=schemas.PostInResponse)
def update_post(
    *,
    id: int,
    body: schemas.PostUpdate,
    current_user: models.User = Depends(
        authentication.get_current_active_user)
) -> Any:
    """
    Update an post.
    """
    post = post_services.get(id=id, requested_user=current_user)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (not repositories.users.is_superuser(current_user)
            and (post.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post = post_services.update(id=id, body=body, requested_user=current_user)
    return post


@router.get("/{id}", response_model=schemas.PostInResponse)
def read_post_by_id(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user)
) -> Any:
    """
    Get post by ID.
    """
    try:
        post = post_services.get(id=id, requested_user=current_user)
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{id}", response_model=schemas.PostInResponse)
def delete_post(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user)
) -> Any:
    """
    Delete an post.
    """
    try:
        post = post_services.remove(id=id, requested_user=current_user)
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
