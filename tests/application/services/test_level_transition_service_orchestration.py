from unittest.mock import Mock

from src.application.services.level_transition_service import LevelTransitionService
from src.domain.enums.level import Level


def test_transition_orchestrates_normalize_validate_and_decide() -> None:
    policy = Mock()
    validator = Mock()
    normalizer = Mock()

    normalizer.normalize.return_value = Level.JR
    policy.decide.return_value = Level.MID

    service = LevelTransitionService(
        policy=policy,
        validator=validator,
        normalizer=normalizer,
    )

    result = service.transition("JR", [8.0, 9.0, 8.0])

    assert result == Level.MID
    normalizer.normalize.assert_called_once_with("JR")
    validator.validate_recent_scores.assert_called_once_with([8.0, 9.0, 8.0])
    policy.decide.assert_called_once_with(
        current_level=Level.JR,
        recent_scores=[8.0, 9.0, 8.0],
    )