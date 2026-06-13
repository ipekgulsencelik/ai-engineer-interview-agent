from __future__ import annotations

from datetime import datetime

from src.evaluation.ops.evaluators.online_evaluation_pass_evaluator import (
    OnlineEvaluationPassEvaluator,
)
from src.evaluation.ops.factories.online_evaluation_result_factory import (
    OnlineEvaluationResultFactory,
)
from src.evaluation.ops.interpreters.online_evaluation_interpreter import (
    OnlineEvaluationInterpreter,
)
from src.evaluation.ops.value_objects.online_evaluation_result import (
    OnlineEvaluationResult,
)


class OnlineEvaluationEngine:
    """
    Online evaluation orchestration service.
    """

    def __init__(
        self,
        *,
        pass_evaluator: OnlineEvaluationPassEvaluator | None = None,
        interpreter: OnlineEvaluationInterpreter | None = None,
        result_factory: OnlineEvaluationResultFactory | None = None,
    ) -> None:
        self._pass_evaluator = (
            pass_evaluator
            or OnlineEvaluationPassEvaluator()
        )
        self._interpreter = (
            interpreter
            or OnlineEvaluationInterpreter()
        )
        self._result_factory = (
            result_factory
            or OnlineEvaluationResultFactory()
        )

    def evaluate(
        self,
        *,
        request_id: str,
        benchmark_id: str,
        benchmark_name: str,
        model_name: str,
        evaluator_name: str,
        metric_name: str,
        metric_value: float,
        minimum_required_value: float,
        latency_ms: float,
        session_id: str | None = None,
        user_id: str | None = None,
        trace_id: str | None = None,
        experiment_id: str | None = None,
        created_at: datetime | None = None,
        notes: str | None = None,
    ) -> OnlineEvaluationResult:
        passed = self._pass_evaluator.evaluate(
            metric_value=metric_value,
            minimum_required_value=(
                minimum_required_value
            ),
        )

        interpretation = self._interpreter.interpret(
            passed=passed,
        )

        return self._result_factory.create(
            request_id=request_id,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            model_name=model_name,
            evaluator_name=evaluator_name,
            metric_name=metric_name,
            metric_value=metric_value,
            passed=passed,
            latency_ms=latency_ms,
            session_id=session_id,
            user_id=user_id,
            trace_id=trace_id,
            experiment_id=experiment_id,
            interpretation=interpretation,
            created_at=created_at,
            notes=notes,
        )