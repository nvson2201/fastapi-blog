from app.exceptions.base import (
    ObjectNotFound, ObjectDuplicate, ObjectForbidden)


class UserNotFound(ObjectNotFound):
    pass


class UserDuplicate(ObjectDuplicate):
    pass


class UserForbiddenRegiser(ObjectForbidden):
    pass


class UserInvalidCredentials(Exception):
    pass


class UserInactive(Exception):
    pass


class UserNotSuper(Exception):
    pass


class UserIncorrectCredentials(Exception):
    pass
