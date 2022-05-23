from app.services.exceptions.base import ObjectNotFound, ObjectDuplicate


class PostNotFound(ObjectNotFound):
    pass


class PostDuplicate(ObjectDuplicate):
    pass
