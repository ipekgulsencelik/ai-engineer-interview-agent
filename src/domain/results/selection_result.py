from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.domain.entities.question import Question
from src.domain.value_objects.selection_breakdown import (
    SelectionBreakdown,
)
from src.domain.validators.selection_result_validator import (
    SelectionResultValidator,
)


@dataclass(frozen=True, slots=True)
class SelectionResult:
    """
    Question selection pipeline sonucunu temsil eden immutable domain snapshot.

    Bu model:
        - selected question
        - final score
        - explainable scoring breakdown
        - selection telemetry metadata

    taşır.

    Bu model:
        - scoring hesaplamaz
        - ranking yapmaz
        - filtering yapmaz
        - orchestration yönetmez

    Validation:
        SelectionResultValidator tarafından yapılır.
    """

    question: Question
    final_score: float
    breakdown: SelectionBreakdown
    selected_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc,
        ),
    )
    rank: int | None = None
    candidate_count: int | None = None


    def __post_init__(self) -> None:
            SelectionResultValidator.validate(self)