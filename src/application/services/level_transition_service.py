from src.domain.enums.level import Level
from src.domain.normalizers.level_normalizer import DefaultLevelNormalizer, LevelNormalizer
from src.domain.policies.level_transition_policy import LevelTransitionPolicy
from src.domain.validators.level_transition_validator import LevelTransitionValidator


class LevelTransitionService:
    """Orchestration only: normalize -> validate -> decide."""

    def __init__(
        self,
        policy: LevelTransitionPolicy | None = None,
        validator: LevelTransitionValidator | None = None,
        normalizer: LevelNormalizer | None = None,
    ) -> None:
        self._policy = policy or LevelTransitionPolicy()
        self._validator = validator or LevelTransitionValidator()
        self._normalizer = normalizer or DefaultLevelNormalizer()

    def transition(self, current_level: Level | str, recent_scores: list[float]) -> Level:
        normalized_level = self._normalizer.normalize(current_level)
        self._validator.validate_recent_scores(recent_scores)
        return self._policy.decide(current_level=normalized_level, recent_scores=recent_scores)