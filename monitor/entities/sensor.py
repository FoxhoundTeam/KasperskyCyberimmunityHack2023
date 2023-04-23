from .abstract_body import AbstractBody


class SensorBody(AbstractBody):
    message_type_key = "sensor"
    data: float
    sensor_id: int
