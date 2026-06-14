from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)
from src.evaluation.rag.validators.rag_evaluation_report_validator import (
    RAGEvaluationReportValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGEvaluationReport:
    """
    Immutable RAG evaluation report.

    Represents an aggregated report for RAG evaluation
    results across a benchmark, experiment, model, and
    retriever configuration.
    """

    report_id: str

    experiment_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    model_name: str
    retriever_name: str
    evaluator_name: str

    results: tuple[
        RAGEvaluationResult,
        ...,
    ]

    sample_count: int

    average_retrieval_precision: float

    average_retrieval_recall: float

    average_context_relevance_score: float

    average_faithfulness_score: float

    average_answer_relevance_score: float

    average_answer_correctness_score: float

    average_overall_score: float

    hallucination_count: int

    hallucination_rate: float

    passed_count: int

    failed_count: int

    pass_rate: float

    generated_at: datetime

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        RAGEvaluationReportValidator.validate(
            report_id=self.report_id,
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            results=self.results,
            sample_count=self.sample_count,
            average_retrieval_precision=(
                self.average_retrieval_precision
            ),
            average_retrieval_recall=(
                self.average_retrieval_recall
            ),
            average_context_relevance_score=(
                self.average_context_relevance_score
            ),
            average_faithfulness_score=(
                self.average_faithfulness_score
            ),
            average_answer_relevance_score=(
                self.average_answer_relevance_score
            ),
            average_answer_correctness_score=(
                self.average_answer_correctness_score
            ),
            average_overall_score=(
                self.average_overall_score
            ),
            hallucination_count=(
                self.hallucination_count
            ),
            hallucination_rate=(
                self.hallucination_rate
            ),
            passed_count=self.passed_count,
            failed_count=self.failed_count,
            pass_rate=self.pass_rate,
            generated_at=self.generated_at,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def has_results(
        self,
    ) -> bool:
        return bool(
            self.results,
        )

    @property
    def has_hallucinations(
        self,
    ) -> bool:
        return (
            self.hallucination_count > 0
        )

    @property
    def all_passed(
        self,
    ) -> bool:
        return (
            self.sample_count > 0
            and self.passed_count == self.sample_count
        )

    @property
    def has_failures(
        self,
    ) -> bool:
        return (
            self.failed_count > 0
        )