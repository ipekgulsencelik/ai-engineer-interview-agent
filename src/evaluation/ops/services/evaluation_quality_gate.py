from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.quality_gate_result_builder import (
    QualityGateResultBuilder,
)
from src.evaluation.ops.evaluators.quality_gate_evaluator import (
    QualityGateEvaluator,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class EvaluationQualityGate:
    """
    Quality gate orchestration service.
    """

    def evaluate(
        self,
        *,
        gate_name: str,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: float,
        metric_name: str = "overall_score",
        expected_value: float | None = None,
        notes: str | None = None,
    ) -> QualityGateResult:
        actual_value = snapshot.overall_score

        expected_metric_value = (
            minimum_required_score
            if expected_value is None
            else expected_value
        )

        passed = (
            QualityGateEvaluator.evaluate(
                score=snapshot.overall_score,
                minimum_required_score=(
                    minimum_required_score
                ),
            )
        )

        return (
            QualityGateResultBuilder.build(
                gate_name=gate_name,
                snapshot=snapshot,
                metric_name=metric_name,
                actual_value=actual_value,
                expected_value=(
                    expected_metric_value
                ),
                minimum_required_score=(
                    minimum_required_score
                ),
                passed=passed,
                notes=notes,
            )
        )