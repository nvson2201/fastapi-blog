from typing import Any, Dict, List, Optional, Type, Union

from sqlalchemy.orm import Session

from app.decorators.component import (
    ComponentRepository, ModelType, CreateSchemaType, UpdateSchemaType)


class BaseRepository(
        ComponentRepository[ModelType, CreateSchemaType, UpdateSchemaType]
):

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: Any) -> Optional[ModelType]:
        q = self.db.query(self.model)
        q = q.filter(self.model.id == id)
        obj = q.first()

        return obj

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        q = self.db.query(self.model)
        q = q.offset(skip)
        q = q.limit(limit)
        objs = q.all()

        return objs

    def create(self, *, body: CreateSchemaType) -> ModelType:
        if isinstance(body, dict):
            body_dict = body
        else:
            body_dict = body.dict(exclude_unset=True)

        obj = self.model(**body_dict)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def update(
        self,
        obj: ModelType,
        *,
        body: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:

        if isinstance(body, dict):
            update_data = body
        else:
            update_data = body.dict(exclude_unset=True)

        for field in update_data:
            if field in update_data:
                setattr(obj, field, update_data[field])

        self.db.merge(obj)
        self.db.commit()

        return obj

    def remove(self, *, id: int) -> ModelType:
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
