from __future__ import annotations

from src.evaluation.rag.evaluators.context_recall_evaluator import ContextRecallEvaluator
from src.evaluation.rag.value_objects.context_recall_request import ContextRecallRequest


def test_context_recall_evaluator_should_score_expected_context_covered_by_retrieval() -> None:
    assert ContextRecallEvaluator().evaluate(
        request=ContextRecallRequest(
            question="q",
            expected_answer="a",
            expected_context="alpha beta",
            retrieved_context="alpha",
            generated_answer="alpha",
        )
    ) == 0.5
