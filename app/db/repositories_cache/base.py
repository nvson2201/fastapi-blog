from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.plugins.redis import redis_services

from app.decorators.decorator import (
    RepositoryDecorator, ModelType, CreateSchemaType, UpdateSchemaType)
from app.decorators.component import ComponentRepository


class RedisDecorator(RepositoryDecorator[ModelType, CreateSchemaType,
                                         UpdateSchemaType]):

    def __init__(self,  _crud_component: ComponentRepository, prefix: str):
        self._crud_component = _crud_component
        self.prefix = prefix

    def _get_cache(self, id: str):
        return redis_services.get_cache(
            id=str(id),
            prefix=self.prefix
        )

    def _set_cache(self, id: str, data):
        redis_services.set_cache(
            id=str(id),
            prefix=self.prefix,
            data=data.__dict__
        )

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        cache_data = self._get_cache(id)

        if cache_data:
            obj = ModelType(**cache_data)
        else:
            obj = self.crud_component.get(db, id)

        self._set_cache(id, data=obj)

        return obj

    def create(self, db: Session, *, body: CreateSchemaType) -> ModelType:
        obj = self.crud_component.create(db, body=body)
        self._set_cache(id=obj.id, data=obj)

        return obj

    def update(
        self,
        db: Session,
        obj: ModelType,
        *,
        body: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj = self.crud_component.update(db, obj=obj, body=body)
        self._set_cache(id=obj.id, data=obj)
        return obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        pass
