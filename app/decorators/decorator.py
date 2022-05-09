from app.decorators.component import (
    CRUDComponent, ModelType, CreateSchemaType, UpdateSchemaType)


class CRUDDecorator(
        CRUDComponent[ModelType, CreateSchemaType, UpdateSchemaType]
):

    _crud_component: CRUDComponent = None

    def __init__(self, _crud_component: CRUDComponent) -> None:
        self._crud_component = _crud_component

    @property
    def crud_component(self) -> CRUDComponent:
        return self._crud_component

    def get(self):
        self._crud_component.get()

    def create(self):
        self._crud_component.create()

    def update(self):
        self._crud_component.update()

    def remove(self):
        self._crud_component.remove()
