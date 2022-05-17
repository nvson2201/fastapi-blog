from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.db import repositories
from app.api.dependencies import authentication
from app.exceptions.posts import PostNotFound
from app.api.dependencies.post_services import get_post_services
from app.services.posts import PostServices
router = APIRouter()


@router.get("/", response_model=List[schemas.Post])
def read_posts(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    post_services: PostServices = Depends(get_post_services)
) -> Any:
    """
    Retrieve posts.
    """
    posts = post_services.get_multi_by_owner(
        author_id=author_id, skip=skip, limit=limit
    )
    return posts


@router.post("/", response_model=schemas.Post)
def create_post(
    *,
    body: schemas.PostCreate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends(get_post_services)
) -> Any:
    """
    Create new post.
    """
    post = post_services.create_with_owner(
        obj_in=body, author_id=current_user.id)
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    *,
    id: int,
    body: schemas.PostUpdate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends(get_post_services)
) -> Any:
    """
    Update an post.
    """
    post = post_services.get(id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (not repositories.users.is_superuser(current_user)
            and (post.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post = post_services.update(db_obj=post, obj_in=body)
    return post


@router.get("/{id}", response_model=schemas.Post)
def read_post(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends(get_post_services)
) -> Any:
    """
    Get post by ID.
    """
    try:
        post = post_services.get(id=id)
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{id}", response_model=schemas.Post)
def delete_post(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
    post_services: PostServices = Depends(get_post_services)
) -> Any:
    """
    Delete an post.
    """
    try:
        post = post_services.remove(id=id)
    except PostNotFound:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
