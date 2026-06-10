from __future__ import annotations

from src.domain.parsers.implementations.default_level_parser import (
    DefaultLevelParser,
)
from src.domain.parsers.implementations.default_question_category_parser import (
    DefaultQuestionCategoryParser,
)
from src.domain.parsers.implementations.default_question_type_parser import (
    DefaultQuestionTypeParser,
)
from src.domain.parsers.question_field_parser import QuestionFieldParser


class QuestionFieldParserFactory:
    """
    QuestionFieldParser composition factory.
    """

    @staticmethod
    def create_default() -> QuestionFieldParser:
        return QuestionFieldParser(
            level_parser=DefaultLevelParser(),
            category_parser=DefaultQuestionCategoryParser(),
            question_type_parser=DefaultQuestionTypeParser(),
        )