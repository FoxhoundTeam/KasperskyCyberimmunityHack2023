from .abstract_body import AbstractBody


class SensorRequestBody(AbstractBody):
    message_type_key = "sensor_request"
    sensor_id: int
