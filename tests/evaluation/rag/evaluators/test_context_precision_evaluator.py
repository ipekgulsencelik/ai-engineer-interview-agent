from __future__ import annotations

import pytest

from src.evaluation.rag.evaluators.context_precision_evaluator import ContextPrecisionEvaluator
from src.evaluation.rag.value_objects.context_precision_request import ContextPrecisionRequest


def test_context_precision_evaluator_should_score_context_tokens_used_by_answer() -> None:
    assert ContextPrecisionEvaluator().evaluate(
        request=ContextPrecisionRequest(
            question="q",
            generated_answer="grounded answer",
            retrieved_context="grounded answer extra",
            expected_answer="grounded answer",
        )
    ) == pytest.approx(2 / 3)
