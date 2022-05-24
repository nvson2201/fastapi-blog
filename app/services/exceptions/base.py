class ObjectException(Exception):
    pass


class ObjectNotFound(ObjectException):
    pass


class ObjectDuplicate(ObjectException):
    pass


class ObjectForbidden(ObjectException):
    pass
