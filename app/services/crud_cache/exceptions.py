class UserException(Exception):
    pass


class UserNotFound(UserException):
    pass


class UserDuplicate(UserException):
    pass
