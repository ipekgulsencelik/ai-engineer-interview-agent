from __future__ import annotations

import pytest

from src.evaluation.rag.services.rag_metric_evaluation_service import RAGMetricEvaluationService
from tests.evaluation.rag.factories import rag_sample


def test_rag_metric_evaluation_service_should_combine_generation_side_scores() -> None:
    result = RAGMetricEvaluationService().evaluate(
        sample=rag_sample(question="retrieval quality"),
        generated_answer="retrieval context",
        retrieved_context="retrieval context extra",
        model_name="model-a",
        evaluator_name="eval-a",
    )

    assert result.faithfulness_score == 1.0
    assert result.answer_relevance_score == 0.5
    assert result.context_precision_score == pytest.approx(2 / 3)
    assert result.context_relevance_score == result.context_precision_score
    assert result.answer_correctness_score == result.answer_relevance_score
