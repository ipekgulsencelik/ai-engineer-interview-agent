from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.rag.validators.rag_evaluation_result_validator import (
    RagEvaluationResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RagEvaluationResult:
    """
    Immutable RAG evaluation result.

    Represents retrieval-augmented generation evaluation
    output including retrieval, grounding, faithfulness,
    and answer quality signals.
    """

    result_id: str

    experiment_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    sample_id: str

    model_name: str
    retriever_name: str
    evaluator_name: str

    query: str

    generated_answer: str

    expected_answer: str | None = None

    retrieved_context_count: int

    relevant_context_count: int

    retrieval_precision: float

    retrieval_recall: float

    context_relevance_score: float

    faithfulness_score: float

    answer_relevance_score: float

    answer_correctness_score: float

    overall_score: float

    hallucination_detected: bool

    passed: bool

    latency_ms: float

    created_at: datetime

    interpretation: str

    notes: str | None = None

    @property
    def failed(
        self,
    ) -> bool:
        return not self.passed

    @property
    def has_expected_answer(
        self,
    ) -> bool:
        return (
            self.expected_answer
            is not None
        )

    @property
    def has_hallucination(
        self,
    ) -> bool:
        return self.hallucination_detected

    @property
    def context_hit_rate(
        self,
    ) -> float:
        if self.retrieved_context_count == 0:
            return 0.0

        return (
            self.relevant_context_count
            / self.retrieved_context_count
        )

    def __post_init__(
        self,
    ) -> None:
        RAGEvaluationResultValidator.validate(
            result_id=self.result_id,
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            sample_id=self.sample_id,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            query=self.query,
            generated_answer=self.generated_answer,
            expected_answer=self.expected_answer,
            retrieved_context_count=self.retrieved_context_count,
            relevant_context_count=self.relevant_context_count,
            retrieval_precision=self.retrieval_precision,
            retrieval_recall=self.retrieval_recall,
            context_relevance_score=self.context_relevance_score,
            faithfulness_score=self.faithfulness_score,
            answer_relevance_score=self.answer_relevance_score,
            answer_correctness_score=self.answer_correctness_score,
            overall_score=self.overall_score,
            hallucination_detected=self.hallucination_detected,
            passed=self.passed,
            latency_ms=self.latency_ms,
            created_at=self.created_at,
            interpretation=self.interpretation,
            notes=self.notes,
        )