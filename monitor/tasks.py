import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from config import settings
from logging_utils import logger
from monitor import Monitor
from monitor.exceptions import BaseMonitorException

dramatiq.set_broker(RabbitmqBroker(url=settings.broker_uri))


@dramatiq.actor
def monitor(data: str):
    try:
        Monitor(data).validate_and_send()
    except BaseMonitorException as e:
        logger.warning("invalid message", detail=str(e), message=data)
