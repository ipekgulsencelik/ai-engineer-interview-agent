from __future__ import annotations

from src.domain.enums.question_type import QuestionType
from src.domain.normalizers.implementations.snake_case_enum_value_normalizer import (
    SnakeCaseEnumValueNormalizer,
)
from src.domain.parsers.implementations.default_enum_parser import DefaultEnumParser


class DefaultQuestionTypeParser(DefaultEnumParser[QuestionType]):
    """
    Default QuestionType parser.
    """

    def __init__(self) -> None:
        super().__init__(
            enum_class=QuestionType,
            field_name="question_type",
            normalizer=SnakeCaseEnumValueNormalizer(),
        )