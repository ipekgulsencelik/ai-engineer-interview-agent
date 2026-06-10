from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.significance_test_result_schema import (
    SIGNIFICANCE_TEST_RESULT_SCHEMA,
)


class SignificanceTestResultValidator:
    """
    SignificanceTestResult validation service.
    """

    @staticmethod
    def validate(
        *,
        test_name: str,
        statistic: float,
        p_value: float,
        alpha: float,
        is_significant: bool,
        sample_count: int,
        effect_size: float | None = None,
        interpretation: str | None = None,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "test_name": test_name,
                "statistic": statistic,
                "p_value": p_value,
                "alpha": alpha,
                "is_significant": is_significant,
                "sample_count": sample_count,
                "effect_size": effect_size,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=SIGNIFICANCE_TEST_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )