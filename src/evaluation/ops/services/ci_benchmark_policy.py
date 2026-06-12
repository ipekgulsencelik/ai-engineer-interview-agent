from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.ci_benchmark_policy_result_builder import (
    CIBenchmarkPolicyResultBuilder,
)
from src.evaluation.ops.constants.ci_policy import (
    MINIMUM_OVERALL_SCORE_GATE_NAME,
)
from src.evaluation.ops.evaluators.blocking_failure_counter import (
    BlockingFailureCounter,
)
from src.evaluation.ops.evaluators.ci_policy_evaluator import (
    CIPolicyEvaluator,
)
from src.evaluation.ops.services.evaluation_quality_gate import (
    EvaluationQualityGate,
)
from src.evaluation.ops.validators.ci_benchmark_policy_input_validator import (
    CIBenchmarkPolicyInputValidator,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class CIBenchmarkPolicy:
    """
    CI benchmark policy orchestration service.
    """

    def __init__(
        self,
        *,
        quality_gate: EvaluationQualityGate | None = None,
    ) -> None:
        self._quality_gate = (
            quality_gate
            or EvaluationQualityGate()
        )

    def evaluate(
        self,
        *,
        policy_name: str,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float,
        additional_gate_results: Sequence[QualityGateResult] = (),
        notes: str | None = None,
    ) -> CIBenchmarkPolicyResult:
        CIBenchmarkPolicyInputValidator.validate(
            snapshot=snapshot,
            additional_gate_results=additional_gate_results,
        )

        score_gate = self._quality_gate.evaluate(
            gate_name=MINIMUM_OVERALL_SCORE_GATE_NAME,
            snapshot=snapshot,
            minimum_required_score=minimum_required_score,
            notes=notes,
        )

        gate_results = (
            score_gate,
            *tuple(additional_gate_results),
        )

        blocking_failure_count = BlockingFailureCounter.count(
            gate_results=gate_results,
        )

        deployment_allowed = CIPolicyEvaluator.evaluate(
            blocking_failure_count=blocking_failure_count,
        )

        return CIBenchmarkPolicyResultBuilder.build(
            policy_name=policy_name,
            snapshot=snapshot,
            minimum_required_score=minimum_required_score,
            gate_results=gate_results,
            blocking_failure_count=blocking_failure_count,
            deployment_allowed=deployment_allowed,
            notes=notes,
        )