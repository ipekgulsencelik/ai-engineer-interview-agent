from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.resolvers.quality_gate_severity_resolver import (
    QualityGateSeverityResolver,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class QualityGateResultBuilder:
    """
    Builds QualityGateResult instances.
    """

    @staticmethod
    def build(
        *,
        gate_name: str,
        snapshot: ExperimentResultSnapshot,
        metric_name: str,
        actual_value: float,
        expected_value: float,
        minimum_required_score: float,
        passed: bool,
        notes: str | None = None,
    ) -> QualityGateResult:
        return QualityGateResult(
            gate_name=gate_name,
            benchmark_id=snapshot.benchmark_id,
            benchmark_name=snapshot.benchmark_name,
            benchmark_version=snapshot.benchmark_version,
            experiment_id=snapshot.experiment_id,
            model_name=snapshot.model_name,
            metric_name=metric_name,
            actual_value=actual_value,
            expected_value=expected_value,
            overall_score=snapshot.overall_score,
            minimum_required_score=minimum_required_score,
            passed=passed,
            severity=(
                QualityGateSeverityResolver.resolve(
                    passed=passed,
                )
            ),
            interpretation=(
                "quality_gate_passed"
                if passed
                else "quality_gate_failed"
            ),
            notes=notes,
        )