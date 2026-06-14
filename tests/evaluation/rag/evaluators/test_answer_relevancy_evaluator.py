from __future__ import annotations

from src.evaluation.rag.evaluators.answer_relevancy_evaluator import AnswerRelevancyEvaluator
from src.evaluation.rag.value_objects.answer_relevancy_request import AnswerRelevancyRequest


def test_answer_relevancy_evaluator_should_score_answer_overlap_with_question() -> None:
    assert AnswerRelevancyEvaluator().evaluate(
        request=AnswerRelevancyRequest(
            question="retrieval quality",
            generated_answer="retrieval latency",
        )
    ) == 0.5
