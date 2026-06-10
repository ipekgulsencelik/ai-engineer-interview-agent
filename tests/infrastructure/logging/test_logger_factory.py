import logging

from src.infrastructure.logging.json_formatter import JsonFormatter
from src.infrastructure.logging.logger_factory import LoggerFactory


def test_create_logger_configures_json_stream_handler() -> None:
    logger_name = "unit.test.logger.configured"
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.propagate = False

    configured = LoggerFactory.create_logger(logger_name)

    assert configured.level == logging.INFO
    assert configured.propagate is False
    assert configured.handlers
    assert isinstance(configured.handlers[0].formatter, JsonFormatter)


def test_create_logger_reuses_existing_logger_instance() -> None:
    logger_name = "unit.test.logger.reuse"
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.propagate = False

    first = LoggerFactory.create_logger(logger_name)
    second = LoggerFactory.create_logger(logger_name)

    assert first is second
    assert len(second.handlers) == 1
