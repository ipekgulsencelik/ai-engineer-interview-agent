from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.category_metric_snapshot_schema import (
    CATEGORY_METRIC_SNAPSHOT_SCHEMA,
)
from src.evaluation.metrics.value_objects.agreement_result import (
    AgreementResult,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)
from src.evaluation.metrics.value_objects.regression_metric_result import (
    RegressionMetricResult,
)


class CategoryMetricSnapshotValidator:
    """
    CategoryMetricSnapshot validation service.
    """

    @staticmethod
    def validate(
        *,
        category: str,
        average_human_score: float,
        average_llm_score: float,
        correlation_result: CorrelationResult,
        agreement_result: AgreementResult,
        regression_result: RegressionMetricResult,
        overall_alignment_score: float,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "category": category,
                "average_human_score": average_human_score,
                "average_llm_score": average_llm_score,
                "overall_alignment_score": overall_alignment_score,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=CATEGORY_METRIC_SNAPSHOT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        CategoryMetricSnapshotValidator._validate_metric_results(
            correlation_result=correlation_result,
            agreement_result=agreement_result,
            regression_result=regression_result,
        )

    @staticmethod
    def _validate_metric_results(
        *,
        correlation_result: CorrelationResult,
        agreement_result: AgreementResult,
        regression_result: RegressionMetricResult,
    ) -> None:
        if not isinstance(
            correlation_result,
            CorrelationResult,
        ):
            raise EvaluationValidationError(
                "correlation_result must be CorrelationResult."
            )

        if not isinstance(
            agreement_result,
            AgreementResult,
        ):
            raise EvaluationValidationError(
                "agreement_result must be AgreementResult."
            )

        if not isinstance(
            regression_result,
            RegressionMetricResult,
        ):
            raise EvaluationValidationError(
                "regression_result must be RegressionMetricResult."
            )