from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone

from src.domain.enums.level import Level
from src.domain.validators.interview_state_validator import InterviewStateValidator


@dataclass(frozen=True)
class InterviewState:
    """Immutable interview runtime state snapshot."""

    session_id: str
    candidate_id: str
    current_level: Level
    asked_question_ids: tuple[str, ...] = field(default_factory=tuple)
    recent_scores: tuple[float, ...] = field(default_factory=tuple)
    turn_count: int = 0
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


    def __post_init__(self) -> None:
        InterviewStateValidator.validate_identity(
            session_id=self.session_id,
            candidate_id=self.candidate_id,
        )
        InterviewStateValidator.validate_level(
            self.current_level,
        )

    def with_question_asked(self, *, question_id: str, score: float | None = None) -> "InterviewState":
        normalized_question_id = InterviewStateValidator.validate_question_id(question_id)
        InterviewStateValidator.validate_score(score)

        scores = self.recent_scores
        if score is not None:
            scores = (*scores, float(score))

        return replace(
            self,
            asked_question_ids=(*self.asked_question_ids, normalized_question_id),
            recent_scores=scores,
            turn_count=self.turn_count + 1,
            updated_at=datetime.now(timezone.utc),
        )

    def with_level(self, *, level: Level) -> "InterviewState":
        return replace(
            self,
            current_level=level,
            updated_at=datetime.now(timezone.utc),
        )