from __future__ import annotations

from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
)
from src.evaluation.rag.value_objects.answer_relevancy_request import (
    AnswerRelevancyRequest,
)
from src.evaluation.rag.value_objects.context_precision_request import (
    ContextPrecisionRequest,
)
from src.evaluation.rag.value_objects.context_recall_request import (
    ContextRecallRequest,
)
from src.evaluation.rag.value_objects.faithfulness_evaluation_request import (
    FaithfulnessEvaluationRequest,
)
from src.evaluation.rag.value_objects.retrieval_hit_rate_request import (
    RetrievalHitRateRequest,
)


class RAGSampleRequestFactory:
    """
    Builds metric-specific requests from a RAG sample
    and runtime model/retriever outputs.
    """

    @staticmethod
    def build_faithfulness_request(
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> FaithfulnessEvaluationRequest:
        return FaithfulnessEvaluationRequest(
            question=sample.question,
            generated_answer=generated_answer,
            retrieved_context=retrieved_context,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

    @staticmethod
    def build_answer_relevancy_request(
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        model_name: str,
        evaluator_name: str,
    ) -> AnswerRelevancyRequest:
        return AnswerRelevancyRequest(
            question=sample.question,
            generated_answer=generated_answer,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

    @staticmethod
    def build_context_precision_request(
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> ContextPrecisionRequest:
        return ContextPrecisionRequest(
            question=sample.question,
            generated_answer=generated_answer,
            retrieved_context=retrieved_context,
            expected_answer=sample.expected_answer,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

    @staticmethod
    def build_context_recall_request(
        *,
        sample: RAGEvaluationSample,
        generated_answer: str,
        retrieved_context: str,
        model_name: str,
        evaluator_name: str,
    ) -> ContextRecallRequest | None:
        if sample.expected_context is None:
            return None

        return ContextRecallRequest(
            question=sample.question,
            expected_answer=(
                sample.expected_answer
                or ""
            ),
            expected_context=sample.expected_context,
            retrieved_context=retrieved_context,
            generated_answer=generated_answer,
            model_name=model_name,
            evaluator_name=evaluator_name,
        )

    @staticmethod
    def build_retrieval_hit_rate_request(
        *,
        sample: RAGEvaluationSample,
        retrieved_chunk_ids: tuple[
            str,
            ...,
        ],
        model_name: str,
        retriever_name: str,
    ) -> RetrievalHitRateRequest | None:
        if not sample.expected_chunk_ids:
            return None

        return RetrievalHitRateRequest(
            question=sample.question,
            expected_chunk_id=(
                sample.expected_chunk_ids[0]
            ),
            retrieved_chunk_ids=retrieved_chunk_ids,
            top_k=len(
                retrieved_chunk_ids,
            ),
            expected_context=sample.expected_context,
            retrieved_contexts=(),
            model_name=model_name,
            retriever_name=retriever_name,
        )