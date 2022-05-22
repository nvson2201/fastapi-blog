from typing import Optional
from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    username: Optional[str] = None
    following: bool = False


class ProfileInResponse(BaseModel):
    profile: Profile
