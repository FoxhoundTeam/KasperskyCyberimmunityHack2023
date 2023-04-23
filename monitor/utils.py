from pykafka import KafkaClient

from config import settings


def get_kc() -> KafkaClient:
    return KafkaClient(hosts=settings.kafka_server)
