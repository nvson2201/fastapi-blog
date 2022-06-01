from typing import Optional
from fastapi import Query
from app.config import settings
from app.schemas import PostsFilters


def get_post_filters(
    tags: Optional[str] = None,
    author: Optional[str] = None,
    user_favorited: Optional[str] = None,
    limit: int = Query(settings.DEFAULT_ARTICLES_LIMIT, ge=1),
    offset: int = Query(settings.DEFAULT_ARTICLES_OFFSET, ge=0),
) -> PostsFilters:
    return PostsFilters(
        tags=tags,
        author=author,
        user_favorited=user_favorited,
        limit=limit,
        offset=offset,
    )
