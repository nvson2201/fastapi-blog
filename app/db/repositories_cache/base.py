from typing import Any, Dict, Optional, Union, Type

from app.plugins.redis import redis_services

from app.decorators.decorator import (
    RepositoryDecorator, ModelType, CreateSchemaType, UpdateSchemaType)
from app.decorators.component import ComponentRepository


class RedisDecorator(RepositoryDecorator[ModelType, CreateSchemaType,
                                         UpdateSchemaType]):

    def __init__(self,  model: Type[ModelType],
                 _crud_component: ComponentRepository, prefix: str):
        self.model = model
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

    def _delete_cache(self, id: str):
        redis_services.del_cache(
            id=str(id),
            prefix=self.prefix
        )

    def get(self, id: Any) -> Optional[ModelType]:
        cache_data = self._get_cache(id)
        if cache_data:
            obj = self.model(**cache_data)
        else:
            obj = self.crud_component.get(id)

        self._set_cache(id, data=obj)

        return obj

    def create(self, *, body: CreateSchemaType) -> ModelType:
        obj = self.crud_component.create(body=body)
        self._set_cache(id=obj.id, data=obj)

        return obj

    def update(
        self,
        obj: ModelType,
        *,
        body: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj = self.crud_component.update(obj=obj, body=body)
        self._set_cache(id=obj.id, data=obj)
        return obj

    def remove(self, *, id: int) -> ModelType:
        obj = self.crud_component.remove(id)
        self._delete_cache(id)
        return obj
