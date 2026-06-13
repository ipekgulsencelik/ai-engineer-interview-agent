from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.validators.online_evaluation_result_validator import (
    OnlineEvaluationResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OnlineEvaluationResult:
    """
    Immutable online evaluation result.

    Represents a production-time evaluation outcome
    collected from live model interactions.
    """

    result_id: str

    request_id: str

    benchmark_id: str
    benchmark_name: str

    model_name: str
    evaluator_name: str

    metric_name: str
    metric_value: float

    passed: bool

    latency_ms: float

    created_at: datetime

    session_id: str | None = None

    user_id: str | None = None

    trace_id: str | None = None

    experiment_id: str | None = None

    interpretation: str | None = None

    error_message: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        OnlineEvaluationResultValidator.validate(
            result_id=self.result_id,
            request_id=self.request_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            metric_name=self.metric_name,
            metric_value=self.metric_value,
            passed=self.passed,
            latency_ms=self.latency_ms,
            created_at=self.created_at,
            session_id=self.session_id,
            user_id=self.user_id,
            trace_id=self.trace_id,
            experiment_id=self.experiment_id,
            interpretation=self.interpretation,
            error_message=self.error_message,
            notes=self.notes,
        )

    @property
    def failed(
        self,
    ) -> bool:
        return not self.passed

    @property
    def has_session(
        self,
    ) -> bool:
        return self.session_id is not None

    @property
    def has_user(
        self,
    ) -> bool:
        return self.user_id is not None

    @property
    def has_trace(
        self,
    ) -> bool:
        return self.trace_id is not None

    @property
    def has_experiment(
        self,
    ) -> bool:
        return self.experiment_id is not None

    @property
    def has_error(
        self,
    ) -> bool:
        return self.error_message is not None