from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.constants.interview_state import (
    DEFAULT_TARGET_DIFFICULTY,
)
from src.domain.enums.level import Level
from src.domain.validators.interview_state_validator import (
    InterviewStateValidator,
)


@dataclass(frozen=True, slots=True)
class InterviewState:
    """
    Current adaptive interview snapshot.
    """

    current_level: Level

    asked_question_ids: tuple[str, ...] = field(
        default_factory=tuple,
    )

    recent_scores: tuple[float, ...] = field(
        default_factory=tuple,
    )

    weak_categories: tuple[str, ...] = field(
        default_factory=tuple,
    )

    target_difficulty: int = (
        DEFAULT_TARGET_DIFFICULTY
    )

    def __post_init__(self) -> None:
        InterviewStateValidator.validate(self)