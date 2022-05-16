from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import repositories
from app.api.dependencies import authentication
from app.api.dependencies.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Post])
def read_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Retrieve posts.
    """
    if repositories.user.is_superuser(current_user):
        posts = repositories.post.get_multi(db, skip=skip, limit=limit)
    else:
        posts = repositories.post.get_multi_by_owner(
            db=db, author_id=current_user.id, skip=skip, limit=limit
        )
    return posts


@router.post("/", response_model=schemas.Post)
def create_post(
    *,
    db: Session = Depends(get_db),
    body: schemas.PostCreate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Create new post.
    """
    post = repositories.post.create_with_owner(
        db=db, obj_in=body, author_id=current_user.id)
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    *,
    db: Session = Depends(get_db),
    id: int,
    body: schemas.PostUpdate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Update an post.
    """
    post = repositories.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (not repositories.user.is_superuser(current_user)
            and (post.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post = repositories.post.update(db=db, db_obj=post, obj_in=body)
    return post


@router.get("/{id}", response_model=schemas.Post)
def read_post(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Get post by ID.
    """
    post = repositories.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (not repositories.user.is_superuser(current_user)
            and (post.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return post


@router.delete("/{id}", response_model=schemas.Post)
def delete_post(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Delete an post.
    """
    post = repositories.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if (not repositories.user.is_superuser(current_user)
            and (post.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post = repositories.post.remove(db=db, id=id)
    return post
