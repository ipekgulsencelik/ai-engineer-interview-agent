from __future__ import annotations

from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
)
from src.evaluation.rag.evaluators.context_recall_evaluator import (
    ContextRecallEvaluator,
)
from src.evaluation.rag.evaluators.retrieval_hit_rate_evaluator import (
    RetrievalHitRateEvaluator,
)
from src.evaluation.rag.factories.rag_sample_request_factory import (
    RAGSampleRequestFactory,
)
from src.evaluation.rag.value_objects.rag_retrieval_metric_result import (
    RAGRetrievalMetricResult,
)


class RAGRetrievalMetricService:
    """
    Evaluates retrieval-side RAG metrics.
    """

    def __init__(
        self,
        *,
        request_factory: RAGSampleRequestFactory | None = None,
        context_recall_evaluator: (
            ContextRecallEvaluator | None
        ) = None,
        retrieval_hit_rate_evaluator: (
            RetrievalHitRateEvaluator | None
        ) = None,
    ) -> None:
        self._request_factory = (
            request_factory or RAGSampleRequestFactory()
        )
        self._context_recall_evaluator = (
            context_recall_evaluator
            or ContextRecallEvaluator()
        )
        self._retrieval_hit_rate_evaluator = (
            retrieval_hit_rate_evaluator
            or RetrievalHitRateEvaluator()
        )

    def evaluate(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        retrieved_chunk_ids: tuple[str, ...],
        model_name: str,
        retriever_name: str,
        evaluator_name: str,
    ) -> RAGRetrievalMetricResult:
        retrieval_recall = self._evaluate_context_recall(
            sample=sample,
            generated_answer=generated_answer,
            retrieved_context=retrieved_context,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

        retrieval_precision = self._evaluate_retrieval_hit_rate(
            sample=sample,
            retrieved_chunk_ids=retrieved_chunk_ids,
            model_name=model_name,
            retriever_name=retriever_name,
        )

        return RAGRetrievalMetricResult(
            retrieval_precision=retrieval_precision,
            retrieval_recall=retrieval_recall,
        )

    def _evaluate_context_recall(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> float:
        request = (
            self._request_factory.build_context_recall_request(
                sample=sample,
                generated_answer=generated_answer,
                retrieved_context=retrieved_context,
                model_name=model_name,
                evaluator_name=evaluator_name,
            )
        )

        if request is None:
            return 0.0

        return self._context_recall_evaluator.evaluate(
            request=request,
        )

    def _evaluate_retrieval_hit_rate(
        self,
        *,
        sample: RAGEvaluationSample,
        retrieved_chunk_ids: tuple[str, ...],
        model_name: str,
        retriever_name: str,
    ) -> float:
        request = (
            self._request_factory.build_retrieval_hit_rate_request(
                sample=sample,
                retrieved_chunk_ids=retrieved_chunk_ids,
                model_name=model_name,
                retriever_name=retriever_name,
            )
        )

        if request is None:
            return 0.0

        return self._retrieval_hit_rate_evaluator.evaluate(
            request=request,
        )