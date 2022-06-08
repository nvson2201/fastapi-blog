from app.services.exceptions.base import (
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


class UserLimitSendCode(Exception):
    pass


class InvalidCode(Exception):
    pass


class UserNeedToWaitForNextVerify(Exception):
    pass


class UserBanned(Exception):
    pass


class ExtensionNotSupport(Exception):
    pass
