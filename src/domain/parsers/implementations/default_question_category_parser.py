from __future__ import annotations

from src.domain.enums.question_category import QuestionCategory
from src.domain.normalizers.implementations.question_category_normalizer import (
    QuestionCategoryNormalizer,
)
from src.domain.parsers.implementations.default_enum_parser import DefaultEnumParser
from src.domain.resolvers.implementations.question_category_alias_resolver import (
    QuestionCategoryAliasResolver,
)


class DefaultQuestionCategoryParser(
    DefaultEnumParser[QuestionCategory],
):
    """
    Default QuestionCategory parser.
    """

    def __init__(self) -> None:
        super().__init__(
            enum_class=QuestionCategory,
            field_name="category",
            normalizer=QuestionCategoryNormalizer(),
            resolver=QuestionCategoryAliasResolver(),
        )