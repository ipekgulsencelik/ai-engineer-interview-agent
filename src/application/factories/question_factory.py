from __future__ import annotations

from typing import Any

from src.domain.constants.question import (
    DEFAULT_FOLLOWUP_ALLOWED,
    DEFAULT_MARKET_WEIGHT,
)
from src.domain.entities.question import Question
from src.domain.parsers.question_field_parser import QuestionFieldParser
from src.domain.payloads.question_payload_extractor import (
    QuestionPayloadExtractor,
)


class QuestionFactory:
    """
    Raw question payload'ından domain-safe Question entity üretir.
    """

    def __init__(
        self,
        *,
        field_parser: QuestionFieldParser,
        payload_extractor: QuestionPayloadExtractor,
    ) -> None:
        self._field_parser = field_parser
        self._payload_extractor = payload_extractor

    def create_from_payload(
        self,
        payload: dict[str, Any],
    ) -> Question:
        self._payload_extractor.validate_payload(
            payload=payload,
        )

        return Question(
            id=self._payload_extractor.get_required_string(
                payload=payload,
                key="id",
            ),
            text=self._payload_extractor.get_required_string(
                payload=payload,
                key="text",
            ),
            category=self._field_parser.parse_category(
                self._payload_extractor.get_required_value(
                    payload=payload,
                    key="category",
                ),
            ),
            level=self._field_parser.parse_level(
                self._payload_extractor.get_required_value(
                    payload=payload,
                    key="level",
                ),
            ),
            difficulty=self._payload_extractor.get_required_int(
                payload=payload,
                key="difficulty",
            ),
            question_type=self._field_parser.parse_question_type(
                self._payload_extractor.get_required_value(
                    payload=payload,
                    key="question_type",
                ),
            ),
            expected_points=self._payload_extractor.get_optional_string_list(
                payload=payload,
                key="expected_points",
                default=[],
            ),
            keywords=self._payload_extractor.get_optional_string_list(
                payload=payload,
                key="keywords",
                default=[],
            ),
            followup=self._payload_extractor.get_optional_string(
                payload=payload,
                key="followup",
                default=None,
            ),
            ideal_answer_hint=self._payload_extractor.get_optional_string(
                payload=payload,
                key="ideal_answer_hint",
                default=None,
            ),
            market_weight=self._payload_extractor.get_optional_float(
                payload=payload,
                key="market_weight",
                default=DEFAULT_MARKET_WEIGHT,
            ),
            followup_allowed=self._payload_extractor.get_optional_bool(
                payload=payload,
                key="followup_allowed",
                default=DEFAULT_FOLLOWUP_ALLOWED,
            ),
        )