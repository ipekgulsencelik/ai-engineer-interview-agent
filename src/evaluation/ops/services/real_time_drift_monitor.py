from __future__ import annotations

from datetime import datetime

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.evaluators.drift_alert_trigger_evaluator import (
    DriftAlertTriggerEvaluator,
)
from src.evaluation.ops.evaluators.drift_delta_calculator import (
    DriftDeltaCalculator,
)
from src.evaluation.ops.evaluators.drift_interpretation_evaluator import (
    DriftInterpretationEvaluator,
)
from src.evaluation.ops.evaluators.drift_severity_evaluator import (
    DriftSeverityEvaluator,
)
from src.evaluation.ops.factories.drift_alert_factory import (
    DriftAlertFactory,
)
from src.evaluation.ops.value_objects.drift_alert import (
    DriftAlert,
)


class RealTimeDriftMonitor:
    """
    Real-time drift monitoring orchestration service.
    """

    def __init__(
        self,
        *,
        delta_calculator: (
            DriftDeltaCalculator | None
        ) = None,
        trigger_evaluator: (
            DriftAlertTriggerEvaluator | None
        ) = None,
        severity_evaluator: (
            DriftSeverityEvaluator | None
        ) = None,
        interpretation_evaluator: (
            DriftInterpretationEvaluator | None
        ) = None,
        alert_factory: (
            DriftAlertFactory | None
        ) = None,
    ) -> None:
        self._delta_calculator = (
            delta_calculator
            or DriftDeltaCalculator()
        )

        self._trigger_evaluator = (
            trigger_evaluator
            or DriftAlertTriggerEvaluator()
        )

        self._severity_evaluator = (
            severity_evaluator
            or DriftSeverityEvaluator()
        )

        self._interpretation_evaluator = (
            interpretation_evaluator
            or DriftInterpretationEvaluator()
        )

        self._alert_factory = (
            alert_factory
            or DriftAlertFactory()
        )

    def evaluate(
        self,
        *,
        baseline_snapshot: (
            ExperimentResultSnapshot
        ),
        current_snapshot: (
            ExperimentResultSnapshot
        ),
        drift_threshold: float,
        created_at: datetime | None = None,
        notes: str | None = None,
    ) -> DriftAlert:
        drift_delta = (
            self._delta_calculator.calculate(
                baseline_score=(
                    baseline_snapshot.overall_score
                ),
                current_score=(
                    current_snapshot.overall_score
                ),
            )
        )

        alert_triggered = (
            self._trigger_evaluator.evaluate(
                drift_delta=drift_delta,
                drift_threshold=(
                    drift_threshold
                ),
            )
        )

        severity = (
            self._severity_evaluator.evaluate(
                drift_delta=drift_delta,
                drift_threshold=(
                    drift_threshold
                ),
            )
        )

        interpretation = (
            self._interpretation_evaluator.evaluate(
                drift_delta=drift_delta,
                alert_triggered=(
                    alert_triggered
                ),
            )
        )

        return self._alert_factory.create(
            baseline_snapshot=(
                baseline_snapshot
            ),
            current_snapshot=(
                current_snapshot
            ),
            drift_delta=drift_delta,
            drift_threshold=(
                drift_threshold
            ),
            alert_triggered=(
                alert_triggered
            ),
            severity=severity,
            interpretation=(
                interpretation
            ),
            created_at=created_at,
            notes=notes,
        )