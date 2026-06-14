from __future__ import annotations

from src.application.ports.clock import Clock
from src.infrastructure.time.system_clock import SystemClock

from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
)
from src.evaluation.rag.factories.rag_evaluation_result_factory import (
    RAGEvaluationResultFactory,
)
from src.evaluation.rag.services.rag_metric_evaluation_service import (
    RAGMetricEvaluationService,
)
from src.evaluation.rag.services.rag_result_interpretation_service import (
    RAGResultInterpretationService,
)
from src.evaluation.rag.services.rag_retrieval_metric_service import (
    RAGRetrievalMetricService,
)
from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGSampleEvaluationService:
    """
    Evaluates one RAG sample and returns
    a sample-level RAG evaluation result.
    """

    def __init__(
        self,
        *,
        metric_evaluation_service: (
            RAGMetricEvaluationService | None
        ) = None,
        retrieval_metric_service: (
            RAGRetrievalMetricService | None
        ) = None,
        interpretation_service: (
            RAGResultInterpretationService | None
        ) = None,
        result_factory: RAGEvaluationResultFactory | None = None,
        clock: Clock | None = None,
    ) -> None:
        self._metric_evaluation_service = (
            metric_evaluation_service
            or RAGMetricEvaluationService()
        )
        self._retrieval_metric_service = (
            retrieval_metric_service
            or RAGRetrievalMetricService()
        )
        self._interpretation_service = (
            interpretation_service
            or RAGResultInterpretationService()
        )
        self._result_factory = (
            result_factory or RAGEvaluationResultFactory()
        )
        self._clock = clock or SystemClock()

    def evaluate(
        self,
        *,
        experiment_id: str,
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        retrieved_chunk_ids: tuple[str, ...],
    ) -> RAGEvaluationResult:
        started_at = self._clock.now()

        metric_result = self._metric_evaluation_service.evaluate(
            sample=sample,
            generated_answer=generated_answer,
            retrieved_context=retrieved_context,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

        retrieval_result = self._retrieval_metric_service.evaluate(
            sample=sample,
            generated_answer=generated_answer,
            retrieved_context=retrieved_context,
            retrieved_chunk_ids=retrieved_chunk_ids,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
        )

        outcome = self._interpretation_service.evaluate(
            metric_result=metric_result,
            retrieval_result=retrieval_result,
        )

        completed_at = self._clock.now()

        return self._result_factory.create(
            experiment_id=experiment_id,
            model_name=model_name,
            retriever_name=retriever_name,
            evaluator_name=evaluator_name,
            sample=sample,
            generated_answer=generated_answer,
            retrieved_context_count=1,
            relevant_context_count=(
                1
                if metric_result.context_relevance_score > 0.0
                else 0
            ),
            retrieval_precision=(
                retrieval_result.retrieval_precision
            ),
            retrieval_recall=retrieval_result.retrieval_recall,
            context_relevance_score=(
                metric_result.context_relevance_score
            ),
            faithfulness_score=(
                metric_result.faithfulness_score
            ),
            answer_relevance_score=(
                metric_result.answer_relevance_score
            ),
            answer_correctness_score=(
                metric_result.answer_correctness_score
            ),
            overall_score=outcome.overall_score,
            hallucination_detected=(
                outcome.hallucination_detected
            ),
            passed=outcome.passed,
            latency_ms=(
                completed_at
                - started_at
            ).total_seconds()
            * 1000,
            created_at=completed_at,
            interpretation=outcome.interpretation,
        )