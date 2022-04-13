from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import HTTPException
import hashlib
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate, PostUpdate, Post
from app.models import User
from app.models import Post
from app.db.base import Base

hash = hashlib.sha256()


def get_user(db: Session, user_id: int):
    return db.query(User).get(user_id)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hash.update(user.password.encode("utf-8"))
    hashed_password = hash.hexdigest()

    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, user_id: int):
    db_item = Post(**post.dict(), author_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_object_or_404(db: Session, Model: Base, object_id: int):
    db_object = db.query(Model).filter(Model.id == object_id).first()
    if db_object is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db_object


def update_post(db: Session, post_id: int, updated_fields: PostUpdate):
    db.execute(
        update(Post)
        .where(Post.id == post_id)
        .values(updated_fields.dict(exclude_unset=True))
    )

    db.flush()
    db.commit()
    return updated_fields


def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()
