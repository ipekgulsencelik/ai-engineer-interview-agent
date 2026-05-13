from src.domain.config.level_transition_config import LevelTransitionConfig
from src.domain.constants.levels import LEVEL_ORDER
from src.domain.enums.level import Level


class LevelTransitionPolicy:
    """Business decision logic for interview level transitions."""

    def __init__(self, config: LevelTransitionConfig | None = None) -> None:
        self._config = config or LevelTransitionConfig()

    def decide(self, *, current_level: Level, recent_scores: list[float]) -> Level:
        if not recent_scores:
            return current_level

        recent_window = recent_scores[-self._config.recent_window_size :]
        average_score = self._compute_average(recent_window)
        current_index = LEVEL_ORDER.index(current_level)

        if self._should_upgrade(average_score=average_score, current_index=current_index):
            return LEVEL_ORDER[current_index + 1]

        if self._should_downgrade(average_score=average_score, current_index=current_index):
            return LEVEL_ORDER[current_index - 1]

        return current_level

    @staticmethod
    def _compute_average(scores: list[float]) -> float:
        return sum(scores) / len(scores)

    def _should_upgrade(self, *, average_score: float, current_index: int) -> bool:
        return (
            average_score >= self._config.upgrade_threshold
            and current_index < len(LEVEL_ORDER) - 1
        )

    def _should_downgrade(self, *, average_score: float, current_index: int) -> bool:
        return (
            average_score <= self._config.downgrade_threshold
            and current_index > 0
        )