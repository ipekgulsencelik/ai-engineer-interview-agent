from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.benchmark_trends import (
    VALID_TREND_DIRECTIONS,
)
from src.evaluation.metrics.schemas.benchmark_aggregate_result_schema import (
    BENCHMARK_AGGREGATE_RESULT_SCHEMA,
)


class BenchmarkAggregateResultValidator:
    """
    BenchmarkAggregateResult validation service.
    """

    @staticmethod
    def validate(
        *,
        benchmark_id: str,
        benchmark_version: str,
        experiment_count: int,
        mean_score: float,
        median_score: float,
        min_score: float,
        max_score: float,
        std_deviation: float,
        trend_direction: str,
        best_experiment_id: str,
        worst_experiment_id: str,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "benchmark_id": benchmark_id,
                "benchmark_version": benchmark_version,
                "experiment_count": experiment_count,
                "mean_score": mean_score,
                "median_score": median_score,
                "min_score": min_score,
                "max_score": max_score,
                "std_deviation": std_deviation,
                "trend_direction": trend_direction,
                "best_experiment_id": best_experiment_id,
                "worst_experiment_id": worst_experiment_id,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=BENCHMARK_AGGREGATE_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        BenchmarkAggregateResultValidator._validate_score_bounds(
            min_score=min_score,
            max_score=max_score,
            mean_score=mean_score,
            median_score=median_score,
        )

        BenchmarkAggregateResultValidator._validate_trend_direction(
            trend_direction=trend_direction,
        )

    @staticmethod
    def _validate_score_bounds(
        *,
        min_score: float,
        max_score: float,
        mean_score: float,
        median_score: float,
    ) -> None:
        if min_score > max_score:
            raise EvaluationValidationError(
                "min_score must be less than or equal to max_score."
            )

        if not (
            min_score
            <= mean_score
            <= max_score
        ):
            raise EvaluationValidationError(
                "mean_score must be between min_score and max_score."
            )

        if not (
            min_score
            <= median_score
            <= max_score
        ):
            raise EvaluationValidationError(
                "median_score must be between min_score and max_score."
            )

    @staticmethod
    def _validate_trend_direction(
        *,
        trend_direction: str,
    ) -> None:
        if trend_direction not in VALID_TREND_DIRECTIONS:
            raise EvaluationValidationError(
                "trend_direction is invalid."
            )