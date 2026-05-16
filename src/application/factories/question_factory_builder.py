from __future__ import annotations

from src.application.factories.question_factory import QuestionFactory
from src.domain.parsers.factories.question_field_parser_factory import (
    QuestionFieldParserFactory,
)
from src.domain.payloads.question_payload_extractor import (
    QuestionPayloadExtractor,
)


class QuestionFactoryBuilder:
    """
    QuestionFactory dependency composition builder.
    """

    @staticmethod
    def build_default() -> QuestionFactory:
        return QuestionFactory(
            field_parser=QuestionFieldParserFactory.create_default(),
            payload_extractor=QuestionPayloadExtractor(),
        )