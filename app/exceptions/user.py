from app.exceptions.base import (
    ObjectNotFound, ObjectDuplicate, ObjectForbidden)


class UserNotFound(ObjectNotFound):
    pass


class UserDuplicate(ObjectDuplicate):
    pass


class UserForbiddenRegiser(ObjectForbidden):
    pass
