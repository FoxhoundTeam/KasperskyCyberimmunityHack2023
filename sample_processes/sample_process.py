import json
from base64 import b64encode
from dataclasses import dataclass, field
from datetime import datetime
from functools import partial
from random import randint, uniform
from typing import TYPE_CHECKING, Any

from loguru import logger
from OpenSSL import crypto
from pykafka import KafkaClient

from cofnig import settings
from decorator import ACTIONS, action

if TYPE_CHECKING:
    from OpenSSL.crypto import PKey


def get_kc():
    return KafkaClient(hosts=settings.kafka_server)


def get_pkey():
    return crypto.load_privatekey(crypto.FILETYPE_PEM, settings.private_key)


@action
def protection(**kwargs):
    id = kwargs.get("id")
    result = f"protection enabled on {id}" if randint(1, 100) < 90 else "error"
    return {
        "message_id": kwargs.get("message_id"),
        "message_type": "action_result",
        "data": result,
        "action_type": protection.__name__,
    }


@action
def stop(**kwargs):
    id = kwargs.get("id")
    result = f"stopped {id}" if randint(1, 100) < 90 else "error"
    return {
        "message_id": kwargs.get("message_id"),
        "message_type": "action_result",
        "data": result,
        "action_type": stop.__name__,
    }


@action
def sensor_request(**kwargs):
    sensor_id = kwargs.get("sensor_id")
    sensors_generators = {
        1: partial(randint, 1, 1000),
        2: partial(uniform, -50, 50),
        3: partial(randint, -100, 0),
    }
    generator = sensors_generators.get("id")
    if generator is not None:
        return {
            "message_id": kwargs.get("message_id"),
            "message_type": "sensor",
            "data": generator(),
            "sensor_id": sensor_id,
        }
    else:
        return {
            "message_id": kwargs.get("message_id"),
            "message_type": "action_result",
            "data": f"unknown sensor {sensor_id}",
            "action_type": sensor_request.__name__,
        }


@action
def control(**kwargs):
    data = kwargs.get("data")
    result = f"set {data}" if randint(1, 100) < 90 else "error"
    return {
        "message_id": kwargs.get("message_id"),
        "message_type": "action_result",
        "data": result,
        "action_type": control.__name__,
    }


@dataclass
class Consumer:
    kc: KafkaClient = field(init=False, default_factory=get_kc)
    pkey: "PKey" = field(init=False, default_factory=get_pkey)

    def _get_message(self, data: dict[str, Any], destination: str):
        data["destination"] = destination
        data["timestamp"] = datetime.now().isoformat()
        str_data = json.dumps(data)
        return {
            "signature": b64encode(
                crypto.sign(self.pkey, str_data.encode(), "sha256")
            ).decode(),
            "body": str_data,
            "source": settings.kafka_topic,
        }

    def _get_message_data(self, received_message: dict[str, Any]):
        print(received_message, type(received_message))
        message_type = received_message.get("message_type")
        act = ACTIONS.get(message_type)
        if act is None:
            return {
                "message_id": received_message.get("message_id"),
                "message_type": "action_result",
                "data": "unknown",
                "action_type": message_type,
            }
        return act(**received_message)

    def consume(self):
        topic = self.kc.topics[settings.kafka_topic]
        monitor_topic = self.kc.topics[settings.monitor_topic]

        consumer = topic.get_simple_consumer(consumer_group=settings.monitor_topic)
        producer = monitor_topic.get_producer()

        for message in consumer:
            logger.info("got message {message}", message=message.value.decode())
            received_message = json.loads(message.value)
            producer.produce(
                json.dumps(
                    self._get_message(
                        self._get_message_data(received_message),
                        received_message.get("source"),
                    )
                ).encode()
            )
            logger.info("processed message")
            consumer.commit_offsets()


if __name__ == "__main__":
    logger.info("start sample process")
    Consumer().consume()
