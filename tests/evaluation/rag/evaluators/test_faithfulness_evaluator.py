from __future__ import annotations

import pytest

from src.evaluation.rag.evaluators.faithfulness_evaluator import FaithfulnessEvaluator
from src.evaluation.rag.value_objects.faithfulness_evaluation_request import FaithfulnessEvaluationRequest


def test_faithfulness_evaluator_should_score_generated_answer_tokens_supported_by_context() -> None:
    assert FaithfulnessEvaluator().evaluate(
        request=FaithfulnessEvaluationRequest(
            question="q",
            generated_answer="RAG grounds answers",
            retrieved_context="RAG grounds responses",
        )
    ) == pytest.approx(2 / 3)
