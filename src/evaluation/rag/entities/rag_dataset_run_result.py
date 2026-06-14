from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.rag.entities.rag_evaluation_report import (
    RAGEvaluationReport,
)
from src.evaluation.rag.validators.rag_dataset_run_result_validator import (
    RAGDatasetRunResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGDatasetRunResult:
    """
    Immutable RAG dataset run result.

    Represents the final result of evaluating a full
    RAG dataset run across one benchmark, model,
    retriever, and evaluator configuration.
    """

    run_id: str

    experiment_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    model_name: str
    retriever_name: str
    evaluator_name: str

    report: RAGEvaluationReport

    sample_count: int

    passed_count: int

    failed_count: int

    pass_rate: float

    overall_score: float

    started_at: datetime

    completed_at: datetime

    duration_ms: float

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        RAGDatasetRunResultValidator.validate(
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            report=self.report,
            sample_count=self.sample_count,
            passed_count=self.passed_count,
            failed_count=self.failed_count,
            pass_rate=self.pass_rate,
            overall_score=self.overall_score,
            started_at=self.started_at,
            completed_at=self.completed_at,
            duration_ms=self.duration_ms,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def failed(
        self,
    ) -> bool:
        return self.failed_count > 0

    @property
    def passed(
        self,
    ) -> bool:
        return (
            self.sample_count > 0
            and self.failed_count == 0
        )