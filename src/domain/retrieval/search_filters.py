from __future__ import annotations

from dataclasses import dataclass

from src.domain.enums.level import Level
from src.domain.enums.question_category import (
    QuestionCategory,
)
from src.domain.enums.question_type import (
    QuestionType,
)
from src.domain.validators.search_filters_validator import (
    SearchFiltersValidator,
)


@dataclass(frozen=True, slots=True)
class SearchFilters:
    """
    Semantic retrieval metadata filters.
    """

    category: QuestionCategory | None = None

    level: Level | None = None

    question_type: QuestionType | None = None

    min_difficulty: int | None = None

    max_difficulty: int | None = None

    def __post_init__(self) -> None:
        SearchFiltersValidator.validate(self)