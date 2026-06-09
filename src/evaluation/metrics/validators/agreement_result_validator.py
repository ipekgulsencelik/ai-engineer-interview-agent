from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.agreement_result_schema import (
    AGREEMENT_RESULT_SCHEMA,
)


class AgreementResultValidator:
    """
    AgreementResult validation service.
    """

    @staticmethod
    def validate(
        *,
        metric_name: str,
        kappa_score: float,
        agreement_ratio: float,
        sample_count: int,
        evaluator_count: int,
        method: str,
        is_reliable: bool,
        interpretation: str,
        p_value: float | None = None,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "metric_name": metric_name,
                "kappa_score": kappa_score,
                "agreement_ratio": agreement_ratio,
                "sample_count": sample_count,
                "evaluator_count": evaluator_count,
                "method": method,
                "is_reliable": is_reliable,
                "interpretation": interpretation,
                "p_value": p_value,
                "notes": notes,
            },
            schema=AGREEMENT_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )