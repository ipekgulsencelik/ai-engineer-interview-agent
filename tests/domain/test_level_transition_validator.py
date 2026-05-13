import pytest

from src.domain.validators.level_transition_validator import LevelTransitionValidator


def test_validate_recent_scores_accepts_valid_scores() -> None:
    LevelTransitionValidator.validate_recent_scores([0, 5.5, 10])


@pytest.mark.parametrize("value", [(1, 2), "1,2,3", None])
def test_validate_recent_scores_rejects_non_list(value: object) -> None:
    with pytest.raises(TypeError, match="recent_scores must be a list"):
        LevelTransitionValidator.validate_recent_scores(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [True, "8", object()])
def test_validate_recent_scores_rejects_non_numeric_items(value: object) -> None:
    with pytest.raises(TypeError, match="recent_scores must contain numbers"):
        LevelTransitionValidator.validate_recent_scores([8.0, value])


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_validate_recent_scores_rejects_non_finite_values(value: float) -> None:
    with pytest.raises(ValueError, match="Scores must be finite numbers"):
        LevelTransitionValidator.validate_recent_scores([8.0, value])


@pytest.mark.parametrize("value", [-0.1, 10.1])
def test_validate_recent_scores_rejects_out_of_range_values(value: float) -> None:
    with pytest.raises(ValueError, match="Scores must be between 0 and 10"):
        LevelTransitionValidator.validate_recent_scores([8.0, value])