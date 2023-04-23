from enum import Enum
from typing import Any

from pydantic import validator

from .abstract_body import AbstractBody


class SensorType(str, Enum):
    speed = "speed"
    power = "power"
    temperature = "temperature"


MIN_MAX_SENSOR_TYPE = {
    SensorType.speed: (333, 2900),
    SensorType.power: (1000, 19000),
    SensorType.temperature: (5, 45),
}


class SensorBody(AbstractBody):
    message_type_key = "sensor"
    sensor_id: int
    sensor_type: SensorType
    data: float

    @validator("data")
    def validate_data(cls, v: float, values: dict[str, Any]):
        sensor_type = values.get("sensor_type")
        mi, ma = MIN_MAX_SENSOR_TYPE[sensor_type]
        if mi <= v <= ma:
            return v
        raise ValueError(
            f"Value for {sensor_type} has invalid range, min: {mi}, max {ma}"
        )
