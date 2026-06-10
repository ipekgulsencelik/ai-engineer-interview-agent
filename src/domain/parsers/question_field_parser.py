from __future__ import annotations

from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.parsers.contracts.level_parser import LevelParser
from src.domain.parsers.contracts.question_category_parser import (
    QuestionCategoryParser,
)
from src.domain.parsers.contracts.question_type_parser import (
    QuestionTypeParser,
)


class QuestionFieldParser:
    """
    Question field parser facade.

    Raw enum alanlarını domain-safe enum instance'lara dönüştürür.
    """

    def __init__(
        self,
        *,
        level_parser: LevelParser,
        category_parser: QuestionCategoryParser,
        question_type_parser: QuestionTypeParser,
    ) -> None:
        self._level_parser = level_parser
        self._category_parser = category_parser
        self._question_type_parser = question_type_parser

    def parse_level(
        self,
        value: Level | str,
    ) -> Level:
        return self._level_parser.parse(value)

    def parse_category(
        self,
        value: QuestionCategory | str,
    ) -> QuestionCategory:
        return self._category_parser.parse(value)

    def parse_question_type(
        self,
        value: QuestionType | str,
    ) -> QuestionType:
        return self._question_type_parser.parse(value)