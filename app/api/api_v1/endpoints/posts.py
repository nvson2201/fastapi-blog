from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.post.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=schemas.post.Post)
def read_post(post_id: int, db: Session = Depends(deps.get_db)):
    return crud.get_object_or_404(db, models.Post, object_id=post_id)


@router.post(
    "/users/{user_id}/",
    response_model=schemas.post.Post,
    status_code=status.HTTP_201_CREATED,
)
def create_user_post(
    user_id: int, post: schemas.post.PostCreate, db: Session = Depends(deps.get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return crud.create_post(db=db, post=post, user_id=user_id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(deps.get_db)):
    post = crud.get_object_or_404(db, models.Post, post_id)
    return crud.delete_post(db=db, post=post)


@router.patch("/{post_id}", response_model=schemas.post.PostUpdate)
def update_post(
    post_id: int,
    updated_fields: schemas.post.PostUpdate,
    db: Session = Depends(deps.get_db),
):
    return crud.update_post(db, post_id, updated_fields)
