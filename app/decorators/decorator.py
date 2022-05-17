from app.decorators.component import (
    ComponentRepository, ModelType, CreateSchemaType, UpdateSchemaType)


class RepositoryDecorator(
        ComponentRepository[ModelType, CreateSchemaType, UpdateSchemaType]
):

    _crud_component: ComponentRepository = None

    def __init__(self, _crud_component: ComponentRepository) -> None:
        self._crud_component = _crud_component

    @property
    def crud_component(self) -> ComponentRepository:
        return self._crud_component

    def get(self):
        self._crud_component.get()

    def create(self):
        self._crud_component.create()

    def update(self):
        self._crud_component.update()

    def remove(self):
        self._crud_component.remove()
