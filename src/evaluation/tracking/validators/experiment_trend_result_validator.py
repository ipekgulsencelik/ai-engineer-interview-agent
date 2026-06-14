from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.tracking.enums.experiment_trend_direction import (
    ExperimentTrendDirection,
)
from src.evaluation.tracking.schemas.experiment_trend_result_schema import (
    EXPERIMENT_TREND_RESULT_SCHEMA,
)


class ExperimentTrendResultValidator:
    """
    ExperimentTrendResult validation service.
    """

    @staticmethod
    def validate(
        *,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        run_count: int,
        first_run_id: str,
        latest_run_id: str,
        first_overall_score: float | None,
        latest_overall_score: float | None,
        average_overall_score: float | None,
        overall_score_delta: float | None,
        first_pass_rate: float | None,
        latest_pass_rate: float | None,
        pass_rate_delta: float | None,
        best_run_id: str | None,
        best_overall_score: float | None,
        worst_run_id: str | None,
        worst_overall_score: float | None,
        trend_direction: ExperimentTrendDirection,
        interpretation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "experiment_id": experiment_id,
                "experiment_name": experiment_name,
                "experiment_version": experiment_version,
                "run_count": run_count,
                "first_run_id": first_run_id,
                "latest_run_id": latest_run_id,
                "first_overall_score": first_overall_score,
                "latest_overall_score": latest_overall_score,
                "average_overall_score": (
                    average_overall_score
                ),
                "overall_score_delta": (
                    overall_score_delta
                ),
                "first_pass_rate": first_pass_rate,
                "latest_pass_rate": latest_pass_rate,
                "pass_rate_delta": pass_rate_delta,
                "best_run_id": best_run_id,
                "best_overall_score": best_overall_score,
                "worst_run_id": worst_run_id,
                "worst_overall_score": worst_overall_score,
                "trend_direction": str(
                    trend_direction,
                ),
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=EXPERIMENT_TREND_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            trend_direction,
            ExperimentTrendDirection,
        ):
            raise EvaluationValidationError(
                "trend_direction must be ExperimentTrendDirection."
            )

        if run_count < 1:
            raise EvaluationValidationError(
                "run_count must be greater than zero."
            )

        if (
            first_overall_score is None
            or latest_overall_score is None
        ):
            if overall_score_delta is not None:
                raise EvaluationValidationError(
                    "overall_score_delta must be None when overall scores are missing."
                )
        else:
            expected_delta = (
                latest_overall_score
                - first_overall_score
            )

            if (
                overall_score_delta is None
                or abs(
                    overall_score_delta
                    - expected_delta
                )
                > 1e-6
            ):
                raise EvaluationValidationError(
                    "overall_score_delta mismatch."
                )

        if (
            first_pass_rate is None
            or latest_pass_rate is None
        ):
            if pass_rate_delta is not None:
                raise EvaluationValidationError(
                    "pass_rate_delta must be None when pass rates are missing."
                )
        else:
            expected_pass_rate_delta = (
                latest_pass_rate
                - first_pass_rate
            )

            if (
                pass_rate_delta is None
                or abs(
                    pass_rate_delta
                    - expected_pass_rate_delta
                )
                > 1e-6
            ):
                raise EvaluationValidationError(
                    "pass_rate_delta mismatch."
                )

        if (
            best_run_id is None
        ) != (
            best_overall_score is None
        ):
            raise EvaluationValidationError(
                "best_run_id and best_overall_score must both be present or both be None."
            )

        if (
            worst_run_id is None
        ) != (
            worst_overall_score is None
        ):
            raise EvaluationValidationError(
                "worst_run_id and worst_overall_score must both be present or both be None."
            )

        if (
            best_overall_score is not None
            and worst_overall_score is not None
            and best_overall_score < worst_overall_score
        ):
            raise EvaluationValidationError(
                "best_overall_score cannot be lower than worst_overall_score."
            )