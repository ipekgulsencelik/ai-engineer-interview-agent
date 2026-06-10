from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.schemas.bootstrap_sample_result_schema import (
    BOOTSTRAP_SAMPLE_RESULT_SCHEMA,
)


class BootstrapSampleResultValidator:
    """
    BootstrapSampleResult validation service.
    """

    @staticmethod
    def validate(
        *,
        sample_index: int,
        sample_size: int,
        statistic_value: float,
        seed: int | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_index": sample_index,
                "sample_size": sample_size,
                "statistic_value": statistic_value,
                "seed": seed,
            },
            schema=BOOTSTRAP_SAMPLE_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )