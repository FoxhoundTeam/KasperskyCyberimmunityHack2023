import json
from base64 import b64encode
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from OpenSSL import crypto
from pykafka import KafkaClient

from cofnig import settings

if TYPE_CHECKING:
    from OpenSSL.crypto import PKey


def get_kc():
    return KafkaClient(hosts=settings.kafka_server)


def get_pkey():
    return crypto.load_privatekey(crypto.FILETYPE_PEM, settings.private_key)


@dataclass
class MessageSender:
    kc: KafkaClient = field(init=False, default_factory=get_kc)
    pkey: "PKey" = field(init=False, default_factory=get_pkey)

    def send_message(
        self,
        destination: str,
        message_type: str,
        data: dict[str, Any],
    ) -> str:
        # топик монитора в который будем писать
        monitor_topic = self.kc.topics[settings.monitor_topic]
        data["destination"] = destination
        data["message_type"] = message_type
        data["timestamp"] = datetime.now().isoformat()
        data["message_id"] = str(uuid4())
        str_data = json.dumps(data)

        # получаем объект производителя
        producer = monitor_topic.get_producer()
        producer.produce(
            json.dumps(
                {
                    "signature": b64encode(
                        crypto.sign(self.pkey, str_data.encode(), "sha256")
                    ).decode(),
                    "body": str_data,
                    "source": settings.kafka_topic,
                }
            ).encode()
        )
        return data["message_id"]


@dataclass
class MessageGetter:
    kc: KafkaClient = field(init=False, default_factory=get_kc)

    def consume(self):
        # топик, который слушаем
        topic = self.kc.topics[settings.kafka_topic]
        # получаем объект потребителя
        consumer = topic.get_simple_consumer(consumer_group=settings.monitor_topic)

        for message in consumer:
            print(message.value.decode())
