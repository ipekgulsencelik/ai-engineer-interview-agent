from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.tracking.validators.experiment_comparison_result_validator import (
    ExperimentComparisonResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentComparisonResult:
    """
    Immutable experiment comparison result.

    Represents metric-level differences between
    a baseline experiment run and a candidate
    experiment run.
    """

    baseline_run_id: str

    candidate_run_id: str

    baseline_experiment_id: str

    candidate_experiment_id: str

    baseline_experiment_name: str

    candidate_experiment_name: str

    baseline_experiment_version: str

    candidate_experiment_version: str

    baseline_overall_score: float | None

    candidate_overall_score: float | None

    overall_score_delta: float | None

    baseline_pass_rate: float | None

    candidate_pass_rate: float | None

    pass_rate_delta: float | None

    baseline_sample_count: int | None

    candidate_sample_count: int | None

    sample_count_delta: int | None

    winner_experiment_id: str | None

    interpretation: str

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentComparisonResultValidator.validate(
                        baseline_run_id=self.baseline_run_id,
            candidate_run_id=self.candidate_run_id,
            baseline_experiment_id=(
                self.baseline_experiment_id
            ),
            candidate_experiment_id=(
                self.candidate_experiment_id
            ),
            baseline_experiment_name=(
                self.baseline_experiment_name
            ),
            candidate_experiment_name=(
                self.candidate_experiment_name
            ),
            baseline_experiment_version=(
                self.baseline_experiment_version
            ),
            candidate_experiment_version=(
                self.candidate_experiment_version
            ),
            baseline_overall_score=(
                self.baseline_overall_score
            ),
            candidate_overall_score=(
                self.candidate_overall_score
            ),
            overall_score_delta=(
                self.overall_score_delta
            ),
            baseline_pass_rate=(
                self.baseline_pass_rate
            ),
            candidate_pass_rate=(
                self.candidate_pass_rate
            ),
            pass_rate_delta=(
                self.pass_rate_delta
            ),
            baseline_sample_count=(
                self.baseline_sample_count
            ),
            candidate_sample_count=(
                self.candidate_sample_count
            ),
            sample_count_delta=(
                self.sample_count_delta
            ),
            winner_experiment_id=(
                self.winner_experiment_id
            ),
            interpretation=(
                self.interpretation
            ),
            notes=self.notes,
        )

    @property
    def has_winner(
        self,
    ) -> bool:
        return (
            self.winner_experiment_id
            is not None
        )

    @property
    def candidate_improved(
        self,
    ) -> bool:
        return (
            self.overall_score_delta
            is not None
            and self.overall_score_delta > 0
        )

    @property
    def candidate_regressed(
        self,
    ) -> bool:
        return (
            self.overall_score_delta
            is not None
            and self.overall_score_delta < 0
        )

    @property
    def score_unchanged(
        self,
    ) -> bool:
        return (
            self.overall_score_delta
            is not None
            and self.overall_score_delta == 0
        )

    @property
    def pass_rate_improved(
        self,
    ) -> bool:
        return (
            self.pass_rate_delta
            is not None
            and self.pass_rate_delta > 0
        )

    @property
    def pass_rate_regressed(
        self,
    ) -> bool:
        return (
            self.pass_rate_delta
            is not None
            and self.pass_rate_delta < 0
        )

    @property
    def comparable_scores(
        self,
    ) -> bool:
        return (
            self.baseline_overall_score
            is not None
            and self.candidate_overall_score
            is not None
        )

    @property
    def comparable_pass_rates(
        self,
    ) -> bool:
        return (
            self.baseline_pass_rate
            is not None
            and self.candidate_pass_rate
            is not None
        )

    @property
    def comparable_sample_counts(
        self,
    ) -> bool:
        return (
            self.baseline_sample_count
            is not None
            and self.candidate_sample_count
            is not None
        )

    @property
    def winning_run_id(
        self,
    ) -> str | None:
        if not self.has_winner:
            return None

        if (
            self.winner_experiment_id
            == self.candidate_experiment_id
        ):
            return self.candidate_run_id

        if (
            self.winner_experiment_id
            == self.baseline_experiment_id
        ):
            return self.baseline_run_id

        return None