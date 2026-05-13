import pytest

from src.application.services.level_transition_service import LevelTransitionService
from src.domain.enums.level import Level


@pytest.fixture
def service() -> LevelTransitionService:
    return LevelTransitionService()


def test_transition_upgrades_level_for_high_average(service: LevelTransitionService) -> None:
    assert service.transition("JR", [8.0, 9.0, 8.0]) == Level.MID


def test_transition_downgrades_level_for_low_average(service: LevelTransitionService) -> None:
    assert service.transition("MID", [3.0, 4.0, 4.0]) == Level.JR


def test_transition_keeps_level_for_middle_average(service: LevelTransitionService) -> None:
    assert service.transition("MID", [5.0, 6.0, 7.0]) == Level.MID


def test_transition_does_not_upgrade_above_senior(service: LevelTransitionService) -> None:
    assert service.transition("SENIOR", [9.0, 9.0, 10.0]) == Level.SENIOR


def test_transition_raises_for_invalid_level(service: LevelTransitionService) -> None:
    with pytest.raises(ValueError, match="Invalid current level"):
        service.transition("BEGINNER", [8.0, 9.0, 10.0])