from __future__ import annotations

import pytest

from src.evaluation.rag.calculators.conversation_rag_score_calculator import ConversationRAGScoreCalculator


def test_conversation_rag_score_should_average_turn_scores() -> None:
    assert ConversationRAGScoreCalculator().calculate(
        turn_scores=(1.0, 0.0, 0.5),
    ) == pytest.approx(0.5)
