import pytest

from src.domain.selection.selection_explanation import SelectionExplanation


def test_selection_explanation_can_be_created() -> None:
    explanation = SelectionExplanation(
        question_id="q1",
        final_score=8.5,
        reasons=["Level match", "High market weight"],
        signals={"level_score": 1.0, "market_weight": 0.8},
    )

    assert explanation.question_id == "q1"
    assert explanation.final_score == 8.5
    assert "Level match" in explanation.reasons


def test_selection_explanation_empty_question_id_raises_error() -> None:
    with pytest.raises(ValueError, match="Question id cannot be empty"):
        SelectionExplanation(question_id="", final_score=1)


def test_selection_explanation_negative_score_raises_error() -> None:
    with pytest.raises(ValueError, match="Final score cannot be negative"):
        SelectionExplanation(question_id="q1", final_score=-1)
