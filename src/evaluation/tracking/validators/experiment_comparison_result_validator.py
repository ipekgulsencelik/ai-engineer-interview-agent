from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.schemas.experiment_comparison_result_schema import (
    EXPERIMENT_COMPARISON_RESULT_SCHEMA,
)


class ExperimentComparisonResultValidator:
    """
    ExperimentComparisonResult validation service.
    """

    @staticmethod
    def validate(
        *,
        baseline_run_id: str,
        candidate_run_id: str,
        baseline_experiment_id: str,
        candidate_experiment_id: str,
        baseline_experiment_name: str,
        candidate_experiment_name: str,
        baseline_experiment_version: str,
        candidate_experiment_version: str,
        baseline_overall_score: float | None,
        candidate_overall_score: float | None,
        overall_score_delta: float | None,
        baseline_pass_rate: float | None,
        candidate_pass_rate: float | None,
        pass_rate_delta: float | None,
        baseline_sample_count: int | None,
        candidate_sample_count: int | None,
        sample_count_delta: int | None,
        winner_experiment_id: str | None,
        interpretation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "baseline_run_id": baseline_run_id,
                "candidate_run_id": candidate_run_id,
                "baseline_experiment_id": (
                    baseline_experiment_id
                ),
                "candidate_experiment_id": (
                    candidate_experiment_id
                ),
                "baseline_experiment_name": (
                    baseline_experiment_name
                ),
                "candidate_experiment_name": (
                    candidate_experiment_name
                ),
                "baseline_experiment_version": (
                    baseline_experiment_version
                ),
                "candidate_experiment_version": (
                    candidate_experiment_version
                ),
                "baseline_overall_score": (
                    baseline_overall_score
                ),
                "candidate_overall_score": (
                    candidate_overall_score
                ),
                "overall_score_delta": (
                    overall_score_delta
                ),
                "baseline_pass_rate": baseline_pass_rate,
                "candidate_pass_rate": (
                    candidate_pass_rate
                ),
                "pass_rate_delta": pass_rate_delta,
                "baseline_sample_count": (
                    baseline_sample_count
                ),
                "candidate_sample_count": (
                    candidate_sample_count
                ),
                "sample_count_delta": sample_count_delta,
                "winner_experiment_id": (
                    winner_experiment_id
                ),
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=EXPERIMENT_COMPARISON_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if baseline_run_id == candidate_run_id:
            raise EvaluationValidationError(
                "baseline_run_id cannot equal candidate_run_id."
            )

        if (
            baseline_experiment_id
            == candidate_experiment_id
            and baseline_experiment_version
            == candidate_experiment_version
        ):
            raise EvaluationValidationError(
                "baseline and candidate experiment versions cannot be identical."
            )

        if (
            baseline_overall_score is None
            or candidate_overall_score is None
        ):
            if overall_score_delta is not None:
                raise EvaluationValidationError(
                    "overall_score_delta must be None when scores are missing."
                )
        else:
            expected_delta = (
                candidate_overall_score
                - baseline_overall_score
            )

            if abs(
                overall_score_delta
                - expected_delta
            ) > 1e-6:
                raise EvaluationValidationError(
                    "overall_score_delta mismatch."
                )

        if (
            baseline_pass_rate is None
            or candidate_pass_rate is None
        ):
            if pass_rate_delta is not None:
                raise EvaluationValidationError(
                    "pass_rate_delta must be None when pass rates are missing."
                )
        else:
            expected_pass_rate_delta = (
                candidate_pass_rate
                - baseline_pass_rate
            )

            if abs(
                pass_rate_delta
                - expected_pass_rate_delta
            ) > 1e-6:
                raise EvaluationValidationError(
                    "pass_rate_delta mismatch."
                )

        if (
            baseline_sample_count is None
            or candidate_sample_count is None
        ):
            if sample_count_delta is not None:
                raise EvaluationValidationError(
                    "sample_count_delta must be None when sample counts are missing."
                )
        else:
            expected_sample_count_delta = (
                candidate_sample_count
                - baseline_sample_count
            )

            if (
                sample_count_delta
                != expected_sample_count_delta
            ):
                raise EvaluationValidationError(
                    "sample_count_delta mismatch."
                )

        if (
            winner_experiment_id is not None
            and winner_experiment_id
            not in {
                baseline_experiment_id,
                candidate_experiment_id,
            }
        ):
            raise EvaluationValidationError(
                "winner_experiment_id must be baseline or candidate experiment id."
            )