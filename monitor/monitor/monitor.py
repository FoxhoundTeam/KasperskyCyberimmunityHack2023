import json
from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING

from pydantic.json import pydantic_encoder

from config import settings
from entities import BODY_REGISTRY, BaseInfo, DataContainer
from logging_utils import logger
from utils import get_kc

from .exceptions import (
    InvalidBaseInfoException,
    InvalidBodyException,
    InvalidDataContainerException,
    InvalidPolicyException,
)
from .utils import parse_json

if TYPE_CHECKING:
    from pykafka import KafkaClient


@dataclass
class Monitor:
    data: str
    kc: "KafkaClient" = field(default_factory=get_kc, init=False)

    @cached_property
    def data_container(self) -> DataContainer:
        data = parse_json(self.data)
        try:
            return DataContainer.parse_obj(data)
        except Exception:
            raise InvalidDataContainerException

    @cached_property
    def base_info(self) -> BaseInfo:
        data = parse_json(self.data_container.body)
        try:
            return BaseInfo.parse_obj(data)
        except Exception:
            raise InvalidBaseInfoException

    def _get_body(self):
        data = parse_json(self.data_container.body)
        body_parser = BODY_REGISTRY[self.base_info.message_type]
        try:
            return body_parser.parse_obj(data)
        except Exception:
            raise InvalidBodyException

    def _send_kafka_message(self, topic: str, data: str):
        producer = self.kc.topics[topic].get_producer()
        producer.produce(data.encode())

    def _check_policy(self):
        if (
            self.data_container.source,
            self.base_info.destination,
        ) not in settings.policies:
            raise InvalidPolicyException

    def validate_and_send(self):
        self._check_policy()
        body = self._get_body()
        self._send_kafka_message(
            self.base_info.destination,
            json.dumps(
                {**body.dict(), "source": self.data_container.source},
                default=pydantic_encoder,
            ),
        )
        logger.info(
            "sent message, {source} -> {destination}",
            source=self.data_container.source,
            destination=self.base_info.destination,
        )
