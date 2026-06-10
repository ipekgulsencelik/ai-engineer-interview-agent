from __future__ import annotations

from dataclasses import dataclass

from src.domain.entities.question import Question
from src.domain.validators.search_result_validator import (
    SearchResultValidator,
)


@dataclass(frozen=True, slots=True)
class SearchResult:
    """
    Semantic question retrieval sonucunu temsil eden immutable domain result.
    """

    question: Question
    distance: float
    score: float

    def __post_init__(self) -> None:
        SearchResultValidator.validate(self)