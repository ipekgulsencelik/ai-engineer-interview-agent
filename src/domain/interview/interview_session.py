from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from src.domain.enums.level import Level
from src.domain.results.evaluation_result import (
    EvaluationResult,
)
from src.domain.validators.interview_session_validator import (
    InterviewSessionValidator,
)


@dataclass(frozen=True)
class InterviewSession:
    """Adaptive interview workflow aggregate state."""

    session_id: str
    current_level: Level
    asked_question_ids: tuple[str, ...] = field(default_factory=tuple)
    completed_results: tuple[EvaluationResult, ...] = field(default_factory=tuple)
    recent_scores: tuple[float, ...] = field(default_factory=tuple)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        InterviewSessionValidator.validate(self)

    def with_completed_turn(
        self,
        *,
        question_id: str,
        result: EvaluationResult,
    ) -> "InterviewSession":
        normalized_question_id = question_id.strip()
        if not normalized_question_id:
            raise ValueError("question_id cannot be empty")

        return replace(
            self,
            asked_question_ids=(*self.asked_question_ids, normalized_question_id),
            completed_results=(*self.completed_results, result),
            recent_scores=(*self.recent_scores, float(result.score)),
        )

    def with_level(self, *, level: Level) -> "InterviewSession":
        return replace(
            self,
            current_level=level,
        )
