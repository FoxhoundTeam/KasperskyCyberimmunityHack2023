from .abstract_body import AbstractBody


class ProtectionBody(AbstractBody):
    message_type_key = "protection"
    id: int
