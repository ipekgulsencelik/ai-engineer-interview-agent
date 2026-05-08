import pytest

from src.domain.scoring.scoring_context import ScoringContext


def test_scoring_context_can_be_created_with_defaults() -> None:
    context = ScoringContext()

    assert context.current_level == "JR"
    assert context.cv_skills == []
    assert context.asked_question_ids == []
    assert context.recent_scores == []
    assert context.weak_areas == []


def test_scoring_context_invalid_level_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid current level"):
        ScoringContext(current_level="BEGINNER")


def test_scoring_context_invalid_score_raises_error() -> None:
    with pytest.raises(ValueError, match="Recent scores must be between 0 and 10"):
        ScoringContext(recent_scores=[11])
