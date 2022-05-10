from typing import Generic, TypeVar

from pydantic import BaseModel

from app.plugins.mysql.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDComponent(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def get(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass
