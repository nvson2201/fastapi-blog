from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException


from app import models, schemas
from app.db import repositories
from app.api.dependencies import authentication

router = APIRouter()


@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Retrieve comments.
    """
    if repositories.users.is_superuser(current_user):
        comments = repositories.comment.get_multi(skip=skip, limit=limit)
    else:
        comments = repositories.comment.get_multi_by_owner(
            author_id=current_user.id, skip=skip,
            limit=limit, post_id=post_id
        )
    return comments


@ router.post("/", response_model=schemas.Comment)
def create_comment(
    *,

    post_id: int,
    body: schemas.CommentCreate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),


) -> Any:
    """
    Create new comment.
    """
    comment = repositories.comment.create_with_owner(
        body=body, author_id=current_user.id, post_id=post_id)
    return comment


@ router.put("/{id}", response_model=schemas.Comment)
def update_comment(
    *,
    id: int,
    body: schemas.CommentUpdate,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:

    comment = repositories.comment.get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not repositories.users.is_superuser(current_user) and
            (comment.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = repositories.comment.update(comment, body=body)
    return comment


@router.get("/{id}", response_model=schemas.Comment)
def read_comment(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Get comment by ID.
    """
    comment = repositories.comment.get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not repositories.users.is_superuser(current_user)
            and (comment.author_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return comment


@router.delete("/{id}", response_model=schemas.Comment)
def delete_comment(
    *,
    id: int,
    current_user: models.User = Depends(
        authentication.get_current_active_user),
) -> Any:
    """
    Delete an comment.
    """
    comment = repositories.comment.get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not repositories.users.is_superuser(current_user) and
            comment.author_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = repositories.comment.remove(id)
    return comment
