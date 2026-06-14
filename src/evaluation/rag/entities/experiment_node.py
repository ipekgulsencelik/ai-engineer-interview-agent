from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.rag.validators.experiment_node_validator import (
    ExperimentNodeValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentNode:
    """
    Immutable experiment lineage node.

    Represents a single experiment version inside
    an experiment lineage graph.
    """

    experiment_id: str

    experiment_name: str

    experiment_version: str

    parent_experiment_id: str | None = None

    dataset_id: str | None = None

    dataset_name: str | None = None

    dataset_version: str | None = None

    benchmark_id: str | None = None

    benchmark_name: str | None = None

    benchmark_version: str | None = None

    model_name: str | None = None

    retriever_name: str | None = None

    evaluator_name: str | None = None

    overall_score: float | None = None

    pass_rate: float | None = None

    sample_count: int | None = None

    passed_count: int | None = None

    failed_count: int | None = None

    tags: tuple[
        str,
        ...
    ] = ()

    created_at: datetime

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentNodeValidator.validate(
            experiment_id=self.experiment_id,
            experiment_name=self.experiment_name,
            experiment_version=self.experiment_version,
            parent_experiment_id=(
                self.parent_experiment_id
            ),
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            dataset_version=self.dataset_version,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            overall_score=self.overall_score,
            pass_rate=self.pass_rate,
            sample_count=self.sample_count,
            passed_count=self.passed_count,
            failed_count=self.failed_count,
            tags=self.tags,
            created_at=self.created_at,
            notes=self.notes,
        )

    @property
    def has_parent(
        self,
    ) -> bool:
        return (
            self.parent_experiment_id
            is not None
        )

    @property
    def is_root(
        self,
    ) -> bool:
        return (
            self.parent_experiment_id
            is None
        )

    @property
    def success_rate(
        self,
    ) -> float | None:
        return self.pass_rate

    @property
    def has_results(
        self,
    ) -> bool:
        return (
            self.overall_score
            is not None
        )

    @property
    def has_tags(
        self,
    ) -> bool:
        return bool(
            self.tags,
        )