from __future__ import annotations

from src.evaluation.rag.services.rag_result_interpretation_service import RAGResultInterpretationService
from src.evaluation.rag.value_objects.rag_metric_evaluation_result import RAGMetricEvaluationResult
from src.evaluation.rag.value_objects.rag_retrieval_metric_result import RAGRetrievalMetricResult


def test_rag_result_interpretation_service_should_calculate_outcome_from_metric_and_retrieval_results() -> None:
    outcome = RAGResultInterpretationService().evaluate(
        metric_result=RAGMetricEvaluationResult(
            faithfulness_score=1.0,
            answer_relevance_score=1.0,
            context_precision_score=1.0,
        ),
        retrieval_result=RAGRetrievalMetricResult(
            retrieval_precision=1.0,
            retrieval_recall=1.0,
        ),
    )

    assert outcome.overall_score == 1.0
    assert outcome.hallucination_detected is False
    assert outcome.passed is True
