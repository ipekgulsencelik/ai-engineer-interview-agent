import pytest

from src.services.level_transition_service import LevelTransitionService


def test_level_goes_up_when_average_score_is_high() -> None:
    service = LevelTransitionService()

    assert service.transition("JR", [8, 9, 8]) == "MID"


def test_level_goes_down_when_average_score_is_low() -> None:
    service = LevelTransitionService()

    assert service.transition("MID", [3, 4, 4]) == "JR"


def test_level_stays_same_when_average_score_is_medium() -> None:
    service = LevelTransitionService()

    assert service.transition("MID", [5, 6, 7]) == "MID"


def test_senior_does_not_go_above_senior() -> None:
    service = LevelTransitionService()

    assert service.transition("SENIOR", [9, 9, 10]) == "SENIOR"


def test_invalid_level_raises_error() -> None:
    service = LevelTransitionService()

    with pytest.raises(ValueError, match="Invalid current level"):
        service.transition("BEGINNER", [8, 9, 10])
