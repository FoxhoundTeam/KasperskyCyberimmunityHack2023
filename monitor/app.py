from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from config import settings
from logging_utils import logger
from tasks import monitor
from utils import get_kc

if TYPE_CHECKING:
    from pykafka import KafkaClient


@dataclass
class Consumer:
    kc: "KafkaClient" = field(default_factory=get_kc, init=False)

    def consume(self):
        topic = self.kc.topics[settings.kafka_topic]

        consumer = topic.get_simple_consumer(consumer_group="monitor")

        for message in consumer:
            logger.info("got message", message=message.value.decode())
            monitor.send(message.value.decode())
            consumer.commit_offsets()


if __name__ == "__main__":
    logger.info("starting monitoring")
    try:
        Consumer().consume()
    except KeyboardInterrupt:
        logger.info("monitoring stopped")
        exit(0)
