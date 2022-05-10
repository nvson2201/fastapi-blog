from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.plugins.redis import redis_services
from app.models.user import User

from app.decorators.decorator import (
    CRUDDecorator, ModelType, CreateSchemaType, UpdateSchemaType)
from app.decorators.component import CRUDComponent


class CRUDRedisDecorator(CRUDDecorator[ModelType, CreateSchemaType,
                                       UpdateSchemaType]):

    def __init__(self,  _crud_component: CRUDComponent, suffix: str):
        self._crud_component = _crud_component
        self.suffix = suffix

    def _get_cache(self, id: str):
        return redis_services.get_cache(
            id=str(id),
            suffix=self.suffix
        )

    def _set_cache(self, id: str, data: User):
        redis_services.set_cache(
            id=str(id),
            suffix=self.suffix,
            data=data.__dict__
        )

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        cache_data = self._get_cache(id=id)

        if cache_data:
            obj = ModelType(**cache_data)
        else:
            obj = self.crud_component.get(db=db, id=id)

        self._set_cache(id=id, data=obj)

        return obj

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj = self.crud_component.create(db, obj_in=obj_in)

        self._set_cache(id=obj.id, data=obj)

        return obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj = self.crud_component.update(db, db_obj=db_obj, obj_in=obj_in)
        self._set_cache(id=obj.id, data=obj)
        return obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        pass
