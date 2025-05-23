import atexit
import json
import logging
import logging.config
from logging import LogRecord
from typing import override
import datetime as dt

import yaml

from config import settings


class MyJSONFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord) -> dict[str, str | None]:
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        return message


class ColorFormatter(logging.Formatter):

    level_color = {
        "CRITICAL": "\033[35;1m%s\033[0m",  # Пурпурный, жирный
        "FATAL": "\033[36;1m%s\033[0m",  # Голубой, жирный
        "ERROR": "\033[31;1m%s\033[0m",  # Красный, жирный
        "WARNING": "\033[33;1m%s\033[0m",  # Желтый, жирный
        "WARN": "\033[33;1m%s\033[0m",  # Желтый, жирный
        "INFO": "%s",  # Обычный
        "TRACE": "\033[32m%s\033[0m",  # Синий
        "DEBUG": "\033[34m%s\033[0m",  # Зеленый
    }

    def format(self, record: LogRecord) -> str:
        s = super().format(record)
        try:
            return self.level_color[record.levelname] % s
        except Exception:
            return s


def configure_logger() -> None:
    with open("logging_config.yml", "r", encoding="utf-8") as file:
        logging_config = yaml.safe_load(file)
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    if settings.DEBUG:
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler and hasattr(queue_handler, "listener"):
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
    logger.info("Starting...")
