from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.adaptive_pacing_validator import (
    AdaptivePacingValidator,
)


@dataclass(frozen=True, slots=True)
class AdaptivePacing:
    """
    Adaptive interview pacing snapshot.
    """

    target_difficulty: int
    difficulty_multiplier: float
    should_reduce_difficulty: bool
    should_increase_difficulty: bool

    def __post_init__(self) -> None:
        AdaptivePacingValidator.validate(self)