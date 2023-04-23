from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel

BODY_REGISTRY: dict[str, type["AbstractBody"]] = {}


class AbstractBody(BaseModel):
    message_type_key: ClassVar[str]
    message_id: UUID
    timestamp: datetime
    message_type: str

    def __init_subclass__(cls) -> None:
        BODY_REGISTRY[cls.message_type_key] = cls
        return super().__init_subclass__()
