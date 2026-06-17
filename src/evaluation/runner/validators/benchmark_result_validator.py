from __future__ import annotations

from datetime import datetime
from math import isfinite

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.runner.schemas.benchmark_result_schema import (
    BENCHMARK_RESULT_SCHEMA,
)


class BenchmarkResultValidator:
    """
    BenchmarkResult validation service.
    """

    SUPPORTED_WINNERS = frozenset(
        {
            "baseline",
            "candidate",
            "tie",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        result_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        run_id: str,
        experiment_id: str,
        model_name: str,
        started_at: datetime,
        completed_at: datetime,
        overall_score: float,
        passed: bool,
        sample_count: int,
        passed_count: int,
        failed_count: int,
        duration_ms: float | None,
        pass_rate: float | None,
        average_score: float | None,
        best_score: float | None,
        worst_score: float | None,
        evaluator_name: str | None,
        dataset_id: str | None,
        dataset_name: str | None,
        dataset_version: str | None,
        tenant_id: str | None,
        baseline_run_id: str | None,
        candidate_run_id: str | None,
        score_delta: float | None,
        winner: str | None,
        error_message: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "result_id": result_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "run_id": run_id,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "started_at": started_at,
                "completed_at": completed_at,
                "overall_score": overall_score,
                "passed": passed,
                "sample_count": sample_count,
                "passed_count": passed_count,
                "failed_count": failed_count,
                "duration_ms": duration_ms,
                "pass_rate": pass_rate,
                "average_score": average_score,
                "best_score": best_score,
                "worst_score": worst_score,
                "evaluator_name": evaluator_name,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "dataset_version": dataset_version,
                "tenant_id": tenant_id,
                "baseline_run_id": baseline_run_id,
                "candidate_run_id": candidate_run_id,
                "score_delta": score_delta,
                "winner": winner,
                "error_message": error_message,
                "metadata": metadata or {},
            },
            schema=BENCHMARK_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if completed_at < started_at:
            raise EvaluationValidationError(
                "completed_at cannot be before started_at."
            )

        cls._validate_finite_number(
            value=overall_score,
            field_name="overall_score",
        )

        cls._validate_optional_finite_number(
            value=duration_ms,
            field_name="duration_ms",
        )

        cls._validate_optional_finite_number(
            value=pass_rate,
            field_name="pass_rate",
        )

        cls._validate_optional_finite_number(
            value=average_score,
            field_name="average_score",
        )

        cls._validate_optional_finite_number(
            value=best_score,
            field_name="best_score",
        )

        cls._validate_optional_finite_number(
            value=worst_score,
            field_name="worst_score",
        )

        cls._validate_optional_finite_number(
            value=score_delta,
            field_name="score_delta",
        )

        cls._validate_score_range(
            value=overall_score,
            field_name="overall_score",
        )

        cls._validate_optional_score_range(
            value=pass_rate,
            field_name="pass_rate",
        )

        if duration_ms is not None and duration_ms < 0:
            raise EvaluationValidationError(
                "duration_ms cannot be negative."
            )

        if passed_count + failed_count > sample_count:
            raise EvaluationValidationError(
                "passed_count + failed_count cannot exceed sample_count."
            )

        if pass_rate is not None:
            expected_pass_rate = (
                0.0
                if sample_count == 0
                else passed_count / sample_count
            )

            if abs(pass_rate - expected_pass_rate) > 1e-6:
                raise EvaluationValidationError(
                    "pass_rate does not match passed_count / sample_count."
                )

        if (
            best_score is not None
            and average_score is not None
            and best_score < average_score
        ):
            raise EvaluationValidationError(
                "best_score cannot be lower than average_score."
            )

        if (
            worst_score is not None
            and average_score is not None
            and worst_score > average_score
        ):
            raise EvaluationValidationError(
                "worst_score cannot be greater than average_score."
            )

        cls._validate_comparison_fields(
            baseline_run_id=baseline_run_id,
            candidate_run_id=candidate_run_id,
            score_delta=score_delta,
            winner=winner,
        )

        if metadata is not None:
            cls._validate_metadata(
                metadata=metadata,
            )

    @classmethod
    def _validate_comparison_fields(
        cls,
        *,
        baseline_run_id: str | None,
        candidate_run_id: str | None,
        score_delta: float | None,
        winner: str | None,
    ) -> None:
        has_baseline = (
            baseline_run_id is not None
        )
        has_candidate = (
            candidate_run_id is not None
        )

        if has_baseline != has_candidate:
            raise EvaluationValidationError(
                "baseline_run_id and candidate_run_id must both be provided."
            )

        if (
            score_delta is not None
            and not (
                has_baseline
                and has_candidate
            )
        ):
            raise EvaluationValidationError(
                "score_delta requires baseline_run_id and candidate_run_id."
            )

        if (
            winner is not None
            and winner not in cls.SUPPORTED_WINNERS
        ):
            raise EvaluationValidationError(
                "winner must be one of: baseline, candidate, tie."
            )

        if (
            winner is not None
            and score_delta is None
        ):
            raise EvaluationValidationError(
                "winner requires score_delta."
            )

    @staticmethod
    def _validate_finite_number(
        *,
        value: float,
        field_name: str,
    ) -> None:
        if not isinstance(
            value,
            int | float,
        ) or not isfinite(
            float(
                value,
            )
        ):
            raise EvaluationValidationError(
                f"{field_name} must be a finite number."
            )

    @classmethod
    def _validate_optional_finite_number(
        cls,
        *,
        value: float | None,
        field_name: str,
    ) -> None:
        if value is None:
            return

        cls._validate_finite_number(
            value=value,
            field_name=field_name,
        )

    @staticmethod
    def _validate_score_range(
        *,
        value: float,
        field_name: str,
    ) -> None:
        if value < 0.0 or value > 1.0:
            raise EvaluationValidationError(
                f"{field_name} must be between 0.0 and 1.0."
            )

    @classmethod
    def _validate_optional_score_range(
        cls,
        *,
        value: float | None,
        field_name: str,
    ) -> None:
        if value is None:
            return

        cls._validate_score_range(
            value=value,
            field_name=field_name,
        )

    @staticmethod
    def _validate_metadata(
        *,
        metadata: dict[
            str,
            str,
        ],
    ) -> None:
        for key, value in metadata.items():
            if not isinstance(key, str) or not key.strip():
                raise EvaluationValidationError(
                    "metadata keys must be non-empty strings."
                )

            if not isinstance(value, str):
                raise EvaluationValidationError(
                    "metadata values must be strings."
                )