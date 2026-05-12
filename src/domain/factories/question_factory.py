from __future__ import annotations

from src.domain.constants.question import (
    DEFAULT_FOLLOWUP_ALLOWED,
    DEFAULT_MARKET_WEIGHT,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.parsers.question_field_parser import QuestionFieldParser


class QuestionFactory:
    """
    Raw veya domain-safe input değerlerinden Question entity üretir.

    Factory'nin görevi:
        - string normalize etmek
        - enum parse etmek
        - optional list alanlarını güvenli hale getirmek
        - Question entity creation flow'unu merkezi yönetmek
    """

    @classmethod
    def create(
        cls,
        *,
        id: str,
        text: str,
        category: QuestionCategory | str,
        level: Level | str,
        difficulty: int,
        question_type: QuestionType | str,
        expected_points: list[str] | None = None,
        keywords: list[str] | None = None,
        market_weight: float = DEFAULT_MARKET_WEIGHT,
        followup_allowed: bool = DEFAULT_FOLLOWUP_ALLOWED,
    ) -> Question:
        return Question(
            id=cls._normalize_string(id),
            text=cls._normalize_string(text),
            category=QuestionFieldParser.parse_category(category),
            level=QuestionFieldParser.parse_level(level),
            difficulty=difficulty,
            question_type=QuestionFieldParser.parse_question_type(
                question_type
            ),
            expected_points=cls._normalize_string_list(expected_points),
            keywords=cls._normalize_string_list(keywords),
            market_weight=market_weight,
            followup_allowed=followup_allowed,
        )

    @staticmethod
    def _normalize_string(
        value: str,
    ) -> str:
        if not isinstance(value, str):
            return value

        return value.strip()

    @staticmethod
    def _normalize_string_list(
        value: list[str] | None,
    ) -> list[str]:
        if value is None:
            return []

        return [
            item.strip() if isinstance(item, str) else item
            for item in value
        ]