from __future__ import annotations

from src.evaluation.rag.calculators.answer_relevancy_score_calculator import AnswerRelevancyScoreCalculator


def test_answer_relevancy_score_should_use_question_tokens_as_denominator() -> None:
    assert AnswerRelevancyScoreCalculator().calculate(
        question_tokens={"retrieval", "quality"},
        answer_tokens={"retrieval", "latency"},
    ) == 0.5
