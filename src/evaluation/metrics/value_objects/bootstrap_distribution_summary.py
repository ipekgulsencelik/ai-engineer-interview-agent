from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.bootstrap_distribution_summary_validator import (
    BootstrapDistributionSummaryValidator,
)
from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)
from src.evaluation.metrics.value_objects.confidence_interval import (
    ConfidenceInterval,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BootstrapDistributionSummary:
    """
    Immutable bootstrap distribution summary.

    Represents aggregated bootstrap statistics for a metric.
    """

    metric_name: str

    bootstrap_iterations: int

    mean_score: float
    std_deviation: float

    min_score: float
    max_score: float

    confidence_interval: ConfidenceInterval

    bootstrap_samples: tuple[
        BootstrapSampleResult,
        ...,
    ] = ()

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        BootstrapDistributionSummaryValidator.validate(
            metric_name=self.metric_name,
            bootstrap_iterations=self.bootstrap_iterations,
            mean_score=self.mean_score,
            std_deviation=self.std_deviation,
            min_score=self.min_score,
            max_score=self.max_score,
            confidence_interval=self.confidence_interval,
            bootstrap_samples=self.bootstrap_samples,
            notes=self.notes,
        )

    @property
    def score_range(
        self,
    ) -> float:
        return (
            self.max_score
            - self.min_score
        )

    @property
    def has_samples(
        self,
    ) -> bool:
        return bool(
            self.bootstrap_samples,
        )