from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator

from config import settings

from .abstract_body import BODY_REGISTRY


class BaseInfo(BaseModel):
    timestamp: datetime
    destination: str
    message_type: str
    message_id: UUID

    @validator("message_type")
    def validate_message_type(cls, value: str):
        if value not in BODY_REGISTRY:
            raise ValueError("Invalid message type")
        return value

    @validator("destination")
    def validate_destination(cls, value: str):
        if value not in settings.source_key_map:
            raise ValueError("Invalid destination")
        return value

    @property
    def body_parser(self):
        return BODY_REGISTRY[self.message_type]
