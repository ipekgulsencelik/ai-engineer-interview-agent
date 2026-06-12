from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.quality_gate_result_schema import (
    QUALITY_GATE_RESULT_SCHEMA,
)


class QualityGateResultValidator:
    """
    QualityGateResult validation service.
    """

    @staticmethod
    def validate(
        *,
        gate_name: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        experiment_id: str,
        model_name: str,
        metric_name: str,
        actual_value: float,
        expected_value: float,
        passed: bool,
        severity: str,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "gate_name": gate_name,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "metric_name": metric_name,
                "actual_value": actual_value,
                "expected_value": expected_value,
                "passed": passed,
                "severity": severity,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=QUALITY_GATE_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )
