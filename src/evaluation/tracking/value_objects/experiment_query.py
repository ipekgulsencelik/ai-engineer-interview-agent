from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.experiment_run_status import (
    ExperimentRunStatus,
)
from src.evaluation.tracking.validators.experiment_query_validator import (
    ExperimentQueryValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentQuery:
    """
    Immutable experiment query.

    Represents filtering criteria for searching
    experiment runs, lineage nodes, artifacts,
    and experiment metadata.
    """

    experiment_id: str | None = None

    run_id: str | None = None

    experiment_name: str | None = None

    experiment_version: str | None = None

    dataset_id: str | None = None

    dataset_name: str | None = None

    dataset_version: str | None = None

    benchmark_id: str | None = None

    benchmark_name: str | None = None

    benchmark_version: str | None = None

    model_name: str | None = None

    retriever_name: str | None = None

    evaluator_name: str | None = None

    status: ExperimentRunStatus | None = None

    tag_key: str | None = None

    tag_value: str | None = None

    created_after: datetime | None = None

    created_before: datetime | None = None

    min_overall_score: float | None = None

    max_overall_score: float | None = None

    min_pass_rate: float | None = None

    max_pass_rate: float | None = None

    limit: int | None = None

    offset: int | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentQueryValidator.validate(
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            experiment_name=self.experiment_name,
            experiment_version=self.experiment_version,
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            dataset_version=self.dataset_version,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            status=self.status,
            tag_key=self.tag_key,
            tag_value=self.tag_value,
            created_after=self.created_after,
            created_before=self.created_before,
            min_overall_score=self.min_overall_score,
            max_overall_score=self.max_overall_score,
            min_pass_rate=self.min_pass_rate,
            max_pass_rate=self.max_pass_rate,
            limit=self.limit,
            offset=self.offset,
        )

    @property
    def has_tag_filter(
        self,
    ) -> bool:
        return (
            self.tag_key is not None
            or self.tag_value is not None
        )

    @property
    def has_score_filter(
        self,
    ) -> bool:
        return (
            self.min_overall_score is not None
            or self.max_overall_score is not None
        )

    @property
    def has_pass_rate_filter(
        self,
    ) -> bool:
        return (
            self.min_pass_rate is not None
            or self.max_pass_rate is not None
        )

    @property
    def has_date_filter(
        self,
    ) -> bool:
        return (
            self.created_after is not None
            or self.created_before is not None
        )

    @property
    def has_pagination(
        self,
    ) -> bool:
        return (
            self.limit is not None
            or self.offset is not None
        )