from .abstract_body import AbstractBody


class ControlBody(AbstractBody):
    message_type_key = "control"
    data: int
