from typing import Any

from fastapi import (
    APIRouter, Depends
)

from app.db.repositories.tags import TagRepository
from sqlalchemy.orm import Session
from app.db.db import get_db

router = APIRouter()


@router.get(
    "/",
)
def read_tags(
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve tags
    """
    tags = TagRepository(db).get_all_tags()
    return tags
