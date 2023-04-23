class BaseMonitorException(Exception):
    detail = "Monitor exception"

    def __init__(self, *args):
        if not args:
            args = (self.detail,)
        super().__init__(*args)


class InvalidDataContainerException(BaseMonitorException):
    detail = "Got invalid data container format."


class InvalidBaseInfoException(BaseMonitorException):
    detail = "Got invalid base info format."


class InvalidBodyException(BaseMonitorException):
    detail = "Got invalid body."


class InvalidJSONException(BaseMonitorException):
    detail = "Invalid JSON."


class InvalidPolicyException(BaseMonitorException):
    detail = "Invalid policy."
