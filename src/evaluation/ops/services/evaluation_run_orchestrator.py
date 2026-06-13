from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.evaluation_run_result_builder import (
    EvaluationRunResultBuilder,
)
from src.evaluation.ops.calculators.run_duration_calculator import (
    RunDurationCalculator,
)
from src.evaluation.ops.evaluators.run_success_evaluator import (
    RunSuccessEvaluator,
)
from src.evaluation.ops.ports.evaluation_run_orchestrator_ports import (
    CIBenchmarkPolicyEvaluation,
    CurrentTimeProviding,
    EvaluationRunResultBuilding,
    RunDurationCalculation,
    RunIdGeneration,
    RunSuccessEvaluation,
)
from src.evaluation.ops.providers.run_id_provider import RunIdProvider
from src.evaluation.ops.providers.utc_datetime_provider import UTCDateTimeProvider
from src.evaluation.ops.services.ci_benchmark_policy import CIBenchmarkPolicy
from src.evaluation.ops.value_objects.evaluation_run_result import EvaluationRunResult


class EvaluationRunOrchestrator:
    """
    Evaluation execution orchestrator.
    """

    def __init__(
        self,
        *,
        ci_policy: CIBenchmarkPolicyEvaluation | None = None,
        run_id_provider: RunIdGeneration | None = None,
        clock: CurrentTimeProviding | None = None,
        duration_calculator: RunDurationCalculation | None = None,
        success_evaluator: RunSuccessEvaluation | None = None,
        result_builder: EvaluationRunResultBuilding | None = None,
    ) -> None:
        self._ci_policy = ci_policy or CIBenchmarkPolicy()
        self._run_id_provider = run_id_provider or RunIdProvider()
        self._clock = clock or UTCDateTimeProvider()
        self._duration_calculator = duration_calculator or RunDurationCalculator()
        self._success_evaluator = success_evaluator or RunSuccessEvaluator()
        self._result_builder = result_builder or EvaluationRunResultBuilder()

    def run(
        self,
        *,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float | None = None,
        policy_name: str = "default_ci_benchmark_policy",
        notes: str | None = None,
    ) -> EvaluationRunResult:
        started_at = self._clock.now()

        ci_policy_result = None

        if minimum_required_score is not None:
            ci_policy_result = self._ci_policy.evaluate(
                policy_name=policy_name,
                snapshot=snapshot,
                minimum_required_score=minimum_required_score,
                notes=notes,
            )

        completed_at = self._clock.now()

        duration_seconds = self._duration_calculator.calculate(
            started_at=started_at,
            completed_at=completed_at,
        )
        success = self._success_evaluator.evaluate(
            ci_policy_result=ci_policy_result,
        )

        return self._result_builder.build(
            run_id=self._run_id_provider.generate(),
            snapshot=snapshot,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration_seconds,
            success=success,
            ci_policy_result=ci_policy_result,
            notes=notes,
        )
