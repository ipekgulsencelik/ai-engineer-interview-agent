from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.bootstrap_distribution_summary_schema import (
    BOOTSTRAP_DISTRIBUTION_SUMMARY_SCHEMA,
)
from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)
from src.evaluation.metrics.value_objects.confidence_interval import (
    ConfidenceInterval,
)


class BootstrapDistributionSummaryValidator:
    """
    BootstrapDistributionSummary validation service.
    """

    @staticmethod
    def validate(
        *,
        metric_name: str,
        bootstrap_iterations: int,
        mean_score: float,
        std_deviation: float,
        min_score: float,
        max_score: float,
        confidence_interval: ConfidenceInterval,
        bootstrap_samples: tuple[BootstrapSampleResult, ...],
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "metric_name": metric_name,
                "bootstrap_iterations": bootstrap_iterations,
                "mean_score": mean_score,
                "std_deviation": std_deviation,
                "min_score": min_score,
                "max_score": max_score,
                "notes": notes,
            },
            schema=BOOTSTRAP_DISTRIBUTION_SUMMARY_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if min_score > max_score:
            raise EvaluationValidationError(
                "min_score must be less than or equal to max_score."
            )

        if not isinstance(
            confidence_interval,
            ConfidenceInterval,
        ):
            raise EvaluationValidationError(
                "confidence_interval must be ConfidenceInterval."
            )

        if not isinstance(
            bootstrap_samples,
            tuple,
        ):
            raise EvaluationValidationError(
                "bootstrap_samples must be tuple."
            )

        for index, sample in enumerate(
            bootstrap_samples,
        ):
            if not isinstance(
                sample,
                BootstrapSampleResult,
            ):
                raise EvaluationValidationError(
                    "bootstrap_samples"
                    f"[{index}] must be BootstrapSampleResult."
                )

        if (
            bootstrap_samples
            and len(bootstrap_samples) != bootstrap_iterations
        ):
            raise EvaluationValidationError(
                "bootstrap_samples length must match bootstrap_iterations."
            )