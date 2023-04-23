from .abstract_body import AbstractBody


class ActionResponseBody(AbstractBody):
    message_type_key = "action_result"
    data: str
    action_type: str
