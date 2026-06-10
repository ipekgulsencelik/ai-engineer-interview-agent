from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.ops.validators.regression_detection_result_validator import (
    RegressionDetectionResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RegressionDetectionResult:
    """
    Immutable regression detection result.

    Represents a benchmark regression analysis
    between a baseline experiment and a candidate
    experiment.
    """

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    baseline_experiment_id: str
    candidate_experiment_id: str

    baseline_score: float
    candidate_score: float

    score_delta: float

    regression_threshold: float

    regression_detected: bool

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        RegressionDetectionResultValidator.validate(
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            baseline_experiment_id=(
                self.baseline_experiment_id
            ),
            candidate_experiment_id=(
                self.candidate_experiment_id
            ),
            baseline_score=self.baseline_score,
            candidate_score=self.candidate_score,
            score_delta=self.score_delta,
            regression_threshold=(
                self.regression_threshold
            ),
            regression_detected=(
                self.regression_detected
            ),
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def absolute_score_delta(
        self,
    ) -> float:
        return abs(
            self.score_delta,
        )

    @property
    def improved(
        self,
    ) -> bool:
        return self.score_delta > 0

    @property
    def degraded(
        self,
    ) -> bool:
        return self.score_delta < 0

    @property
    def unchanged(
        self,
    ) -> bool:
        return self.score_delta == 0

    @property
    def score_change_percentage(
        self,
    ) -> float:
        if self.baseline_score == 0:
            return 0.0

        return (
            self.score_delta
            / self.baseline_score
        ) * 100