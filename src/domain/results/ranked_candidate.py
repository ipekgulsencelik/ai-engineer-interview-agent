from __future__ import annotations

from dataclasses import dataclass

from src.domain.entities.question import Question
from src.domain.results.selection_breakdown import (
    SelectionBreakdown,
)
from src.domain.validators.ranked_candidate_validator import (
    RankedCandidateValidator,
)


@dataclass(frozen=True)
class RankedCandidate:
    """
    Ranking pipeline sırasında üretilen immutable candidate snapshot modelidir.

    Bu model:
        - candidate question
        - calculated final score
        - explainable scoring breakdown
        - ranking position

    bilgisini taşır.

    Bu model:
        - ranking yapmaz
        - scoring hesaplamaz
        - selection kararı vermez
        - orchestration yönetmez

    Validation:
        RankedCandidateValidator tarafından yapılır.
    """

    question: Question

    final_score: float

    breakdown: SelectionBreakdown

    rank: int

    def __post_init__(self) -> None:
        RankedCandidateValidator.validate(self)