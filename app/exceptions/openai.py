from exceptions.base import BaseInternalException


class PermissionOIException(BaseInternalException):
    pass


class BadRequestOIException(BaseInternalException):
    pass


class NotFoundOIException(BaseInternalException):
    pass


class RateLimitImageOIException(BaseInternalException):
    pass


class ServerOIException(BaseInternalException):
    pass
