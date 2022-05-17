from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import repositories
from app.api.dependencies import authentication
from app.api.dependencies.database import get_db
router = APIRouter()


@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    post_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(
        authentication.get_current_active_user),

) -> Any:
    """
    Retrieve comments.
    """
    if repositories.user.is_superuser(current_user):
        comments = repositories.comment.get_multi(db, skip=skip, limit=limit)
    else:
        comments = repositories.comment.get_multi_by_owner(
            db=db, author_id=current_user.id, skip=skip,
            limit=limit, post_id=post_id
        )
    return comments


@ router.post("/", response_model=schemas.Comment)
def create_comment(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    body: schemas.CommentCreate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),


) -> Any:
    """
    Create new comment.
    """
    comment = repositories.comment.create_with_owner(
        db=db, obj_in=body, author_id=current_user.id, post_id=post_id)
    return comment


@ router.put("/{id}", response_model=schemas.Comment)
def update_comment(
    *,
    db: Session = Depends(get_db),
    id: int,
    body: schemas.CommentUpdate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Update an comment.
    """
    comment = repositories.comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not repositories.user.is_superuser(current_user) and
            (comment.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = repositories.comment.update(db=db, db_obj=comment, obj_in=body)
    return comment


@router.get("/{id}", response_model=schemas.Comment)
def read_comment(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Get comment by ID.
    """
    comment = repositories.comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not repositories.user.is_superuser(current_user)
            and (comment.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return comment


@router.delete("/{id}", response_model=schemas.Comment)
def delete_comment(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Delete an comment.
    """
    comment = repositories.comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not repositories.user.is_superuser(current_user) and
            comment.author_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = repositories.comment.remove(db=db, id=id)
    return comment
