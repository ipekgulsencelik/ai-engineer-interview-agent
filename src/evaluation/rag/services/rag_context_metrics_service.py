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
from src.evaluation.rag.requests.context_recall_request import (
    ContextRecallRequest,
)
from src.evaluation.rag.requests.retrieval_hit_rate_request import (
    RetrievalHitRateRequest,
)


class RAGContextMetricsService:
    """
    Evaluates retrieval-side RAG metrics.
    """

    def __init__(
        self,
        *,
        context_recall_evaluator: ContextRecallEvaluator | None = None,
        retrieval_hit_rate_evaluator: (
            RetrievalHitRateEvaluator | None
        ) = None,
    ) -> None:
        self._context_recall_evaluator = (
            context_recall_evaluator
            or ContextRecallEvaluator()
        )
        self._retrieval_hit_rate_evaluator = (
            retrieval_hit_rate_evaluator
            or RetrievalHitRateEvaluator()
        )

    def evaluate_context_recall(
        self,
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> float:
        if sample.expected_context is None:
            return 0.0

        return self._context_recall_evaluator.evaluate(
            request=ContextRecallRequest(
                question=sample.question,
                expected_answer=sample.expected_answer or "",
                expected_context=sample.expected_context,
                retrieved_context=retrieved_context,
                generated_answer=generated_answer,
                model_name=model_name,
                evaluator_name=evaluator_name,
            )
        )

    def evaluate_retrieval_hit_rate(
        self,
        *,
        sample: RAGEvaluationSample,
        retrieved_chunk_ids: tuple[str, ...],
        model_name: str,
        retriever_name: str,
    ) -> float:
        if not sample.expected_chunk_ids:
            return 0.0

        return self._retrieval_hit_rate_evaluator.evaluate(
            request=RetrievalHitRateRequest(
                question=sample.question,
                expected_chunk_id=sample.expected_chunk_ids[0],
                retrieved_chunk_ids=retrieved_chunk_ids,
                top_k=len(retrieved_chunk_ids),
                expected_context=sample.expected_context,
                retrieved_contexts=(),
                model_name=model_name,
                retriever_name=retriever_name,
            )
        )