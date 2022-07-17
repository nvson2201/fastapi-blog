from typing import Optional

from pydantic import BaseModel


class TagInResponse(BaseModel):
    id: Optional[int] = None
    tag: Optional[str] = None
