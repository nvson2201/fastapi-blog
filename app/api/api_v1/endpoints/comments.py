from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    post_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),

) -> Any:
    """
    Retrieve comments.
    """
    if crud.user.is_superuser(current_user):
        comments = crud.comment.get_multi(db, skip=skip, limit=limit)
    else:
        comments = crud.comment.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip,
            limit=limit, contain_id=post_id
        )
    return comments


@ router.post("/", response_model=schemas.Comment)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    body: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),


) -> Any:
    """
    Create new comment.
    """
    comment = crud.comment.create_with_owner(
        db=db, obj_in=body, owner_id=current_user.id, contain_id=post_id)
    return comment


@ router.put("/{id}", response_model=schemas.Comment)
def update_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    body: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an comment.
    """
    comment = crud.comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not crud.user.is_superuser(current_user) and
            (comment.owner_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = crud.comment.update(db=db, db_obj=comment, obj_in=body)
    return comment


@router.get("/{id}", response_model=schemas.Comment)
def read_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get comment by ID.
    """
    comment = crud.comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not crud.user.is_superuser(current_user)
            and (comment.owner_id != current_user.id)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return comment


@router.delete("/{id}", response_model=schemas.Comment)
def delete_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an comment.
    """
    comment = crud.comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if (not crud.user.is_superuser(current_user) and
            comment.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = crud.comment.remove(db=db, id=id)
    return comment
