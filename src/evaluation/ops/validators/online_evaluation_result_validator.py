from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.online_evaluation_result_schema import (
    ONLINE_EVALUATION_RESULT_SCHEMA,
)


class OnlineEvaluationResultValidator:
    """
    OnlineEvaluationResult validation service.
    """

    @staticmethod
    def validate(
        *,
        result_id: str,
        request_id: str,
        benchmark_id: str,
        benchmark_name: str,
        model_name: str,
        evaluator_name: str,
        metric_name: str,
        metric_value: float,
        passed: bool,
        latency_ms: float,
        created_at: datetime,
        session_id: str | None,
        user_id: str | None,
        trace_id: str | None,
        experiment_id: str | None,
        interpretation: str | None,
        error_message: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "result_id": result_id,
                "request_id": request_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "metric_name": metric_name,
                "metric_value": metric_value,
                "passed": passed,
                "latency_ms": latency_ms,
                "created_at": created_at,
                "session_id": session_id,
                "user_id": user_id,
                "trace_id": trace_id,
                "experiment_id": experiment_id,
                "interpretation": interpretation,
                "error_message": error_message,
                "notes": notes,
            },
            schema=ONLINE_EVALUATION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )
