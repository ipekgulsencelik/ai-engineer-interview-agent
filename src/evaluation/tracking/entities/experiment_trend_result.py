from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.tracking.enums.experiment_trend_direction import (
    ExperimentTrendDirection,
)
from src.evaluation.tracking.validators.experiment_trend_result_validator import (
    ExperimentTrendResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentTrendResult:
    """
    Immutable experiment trend result.

    Represents score and pass-rate trend analysis
    across multiple experiment runs.
    """

    experiment_id: str

    experiment_name: str

    experiment_version: str

    run_count: int

    first_run_id: str

    latest_run_id: str

    first_overall_score: float | None

    latest_overall_score: float | None

    average_overall_score: float | None

    overall_score_delta: float | None

    first_pass_rate: float | None

    latest_pass_rate: float | None

    pass_rate_delta: float | None

    best_run_id: str | None

    best_overall_score: float | None

    worst_run_id: str | None

    worst_overall_score: float | None

    trend_direction: ExperimentTrendDirection

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentTrendResultValidator.validate(
            experiment_id=self.experiment_id,
            experiment_name=self.experiment_name,
            experiment_version=self.experiment_version,
            run_count=self.run_count,
            first_run_id=self.first_run_id,
            latest_run_id=self.latest_run_id,
            first_overall_score=self.first_overall_score,
            latest_overall_score=self.latest_overall_score,
            average_overall_score=(
                self.average_overall_score
            ),
            overall_score_delta=(
                self.overall_score_delta
            ),
            first_pass_rate=self.first_pass_rate,
            latest_pass_rate=self.latest_pass_rate,
            pass_rate_delta=self.pass_rate_delta,
            best_run_id=self.best_run_id,
            best_overall_score=self.best_overall_score,
            worst_run_id=self.worst_run_id,
            worst_overall_score=self.worst_overall_score,
            trend_direction=self.trend_direction,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def score_improved(
        self,
    ) -> bool:
        return (
            self.overall_score_delta is not None
            and self.overall_score_delta > 0
        )

    @property
    def score_regressed(
        self,
    ) -> bool:
        return (
            self.overall_score_delta is not None
            and self.overall_score_delta < 0
        )

    @property
    def pass_rate_improved(
        self,
    ) -> bool:
        return (
            self.pass_rate_delta is not None
            and self.pass_rate_delta > 0
        )

    @property
    def pass_rate_regressed(
        self,
    ) -> bool:
        return (
            self.pass_rate_delta is not None
            and self.pass_rate_delta < 0
        )

    @property
    def has_best_run(
        self,
    ) -> bool:
        return (
            self.best_run_id is not None
        )

    @property
    def has_worst_run(
        self,
    ) -> bool:
        return (
            self.worst_run_id is not None
        )

    @property
    def is_improving(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == ExperimentTrendDirection.IMPROVING
        )

    @property
    def is_regressing(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == ExperimentTrendDirection.REGRESSING
        )

    @property
    def is_stable(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == ExperimentTrendDirection.STABLE
        )

    @property
    def is_volatile(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == ExperimentTrendDirection.VOLATILE
        )

    @property
    def is_unknown(
        self,
    ) -> bool:
        return (
            self.trend_direction
            == ExperimentTrendDirection.UNKNOWN
        )