from app.exceptions.base import ObjectNotFound, ObjectDuplicate


class PostNotFound(ObjectNotFound):
    pass


class PostDuplicate(ObjectDuplicate):
    pass
