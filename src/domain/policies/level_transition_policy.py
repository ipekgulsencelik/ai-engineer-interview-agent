from __future__ import annotations

from src.domain.config.level_transition_config import (
    LevelTransitionConfig,
)
from src.domain.enums.level import Level
from src.domain.policies.level_progression_policy import (
    LevelProgressionPolicy,
)
from src.domain.policies.recent_score_average_policy import (
    RecentScoreAveragePolicy,
)


class LevelTransitionPolicy:
    """
    Adaptive interview level transition policy.
    """

    def __init__(
        self,
        config: LevelTransitionConfig | None = None,
    ) -> None:
        self._config = (
            config
            or LevelTransitionConfig()
        )

    def decide(
        self,
        *,
        current_level: Level,
        recent_scores: list[float],
    ) -> Level:
        if not recent_scores:
            return current_level

        recent_window = recent_scores[
            -self._config.recent_window_size :
        ]

        average_score = (
            RecentScoreAveragePolicy.calculate(
                scores=recent_window,
            )
        )

        if self._should_upgrade(
            average_score=average_score,
        ):
            return (
                LevelProgressionPolicy.upgrade(
                    current_level=current_level,
                )
            )

        if self._should_downgrade(
            average_score=average_score,
        ):
            return (
                LevelProgressionPolicy.downgrade(
                    current_level=current_level,
                )
            )

        return current_level

    def _should_upgrade(
        self,
        *,
        average_score: float,
    ) -> bool:
        return (
            average_score
            >= self._config.upgrade_threshold
        )

    def _should_downgrade(
        self,
        *,
        average_score: float,
    ) -> bool:
        return (
            average_score
            <= self._config.downgrade_threshold
        )