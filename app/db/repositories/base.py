from typing import Any, Dict, List, Optional, Type, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.decorators.component import (
    ComponentRepository, ModelType, CreateSchemaType, UpdateSchemaType)


class BaseRepository(ComponentRepository[ModelType, CreateSchemaType,
                                         UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to
        Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, body: CreateSchemaType) -> ModelType:
        body_dict = jsonable_encoder(body)
        obj = self.model(**body_dict)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(
        self,
        db: Session,
        obj: ModelType,
        *,
        body: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_dict = jsonable_encoder(obj)

        if isinstance(body, dict):
            update_data = body
        else:
            update_data = body.dict(exclude_unset=True)

        for field in obj_dict:
            if field in update_data:
                setattr(obj, field, update_data[field])
        db.merge(obj)
        db.commit()

        return obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
