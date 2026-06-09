from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.evaluator_alignment_report_schema import (
    EVALUATOR_ALIGNMENT_REPORT_SCHEMA,
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


class EvaluatorAlignmentReportValidator:
    """
    EvaluatorAlignmentReport validation service.
    """

    @staticmethod
    def validate(
        *,
        report_id: str,
        evaluator_id: str,
        model_name: str,
        pearson_correlation: CorrelationResult,
        agreement_result: AgreementResult,
        regression_result: RegressionMetricResult,
        overall_alignment_score: float,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "report_id": report_id,
                "evaluator_id": evaluator_id,
                "model_name": model_name,
                "overall_alignment_score": overall_alignment_score,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=EVALUATOR_ALIGNMENT_REPORT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            pearson_correlation,
            CorrelationResult,
        ):
            raise EvaluationValidationError(
                "pearson_correlation must be CorrelationResult."
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