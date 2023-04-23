import sys
from typing import TYPE_CHECKING

from loguru import logger as loguru_logger
from opensearch_logger import OpenSearchHandler

from config import settings

if TYPE_CHECKING:
    from loguru import Logger


logger: "Logger" = loguru_logger.bind(name="json_logger")
logger.remove()
logger.add(sys.stdout, format="{level} {message}", serialize=True, backtrace=True)
handler = OpenSearchHandler(
    index_name="monitor-logs",
    hosts=[settings.opensearch_uri],
    http_auth=(settings.opensearch_username, settings.opensearch_password),
)
logger.add(
    handler,
    format="{level} {message}",
    serialize=True,
    backtrace=False,
    diagnose=False,
)
