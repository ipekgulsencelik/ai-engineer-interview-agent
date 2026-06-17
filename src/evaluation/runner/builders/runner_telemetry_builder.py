from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.runner.entities.runner_execution_result import (
    RunnerExecutionResult,
)


class RunnerTelemetryBuilder:
    """
    Builds telemetry metrics from runner execution results.
    """

    def build(
        self,
        *,
        result: RunnerExecutionResult,
        tenant_id: str | None = None,
    ) -> tuple[
        TelemetryMetric,
        ...,
    ]:
        metrics: list[
            TelemetryMetric
        ] = []

        recorded_at = result.completed_at or datetime.now(
            UTC,
        )

        labels = {
            "runner_id": result.runner_id,
            "runner_name": result.runner_name,
            "status": result.status,
        }

        if result.duration_ms is not None:
            metrics.append(
                self._metric(
                    name="runner.duration_ms",
                    value=result.duration_ms,
                    unit="ms",
                    source=result.runner_name,
                    recorded_at=recorded_at,
                    labels=labels,
                    result=result,
                    tenant_id=tenant_id,
                )
            )

        metrics.append(
            self._metric(
                name="runner.success",
                value=1.0 if result.success else 0.0,
                unit="count",
                source=result.runner_name,
                recorded_at=recorded_at,
                labels=labels,
                result=result,
                tenant_id=tenant_id,
            )
        )

        if result.score is not None:
            metrics.append(
                self._metric(
                    name="runner.score",
                    value=result.score,
                    unit="score",
                    source=result.runner_name,
                    recorded_at=recorded_at,
                    labels=labels,
                    result=result,
                    tenant_id=tenant_id,
                )
            )

        return tuple(
            metrics,
        )

    @staticmethod
    def _metric(
        *,
        name: str,
        value: float,
        unit: str,
        source: str,
        recorded_at: datetime,
        labels: dict[str, str],
        result: RunnerExecutionResult,
        tenant_id: str | None,
    ) -> TelemetryMetric:
        return TelemetryMetric(
            metric_id=str(
                uuid4(),
            ),
            metric_name=name,
            metric_value=value,
            unit=unit,
            source=source,
            recorded_at=recorded_at,
            labels=labels,
            tenant_id=tenant_id,
            experiment_id=result.experiment_id,
            run_id=result.run_id,
            worker_id=result.worker_id,
            correlation_id=result.correlation_id,
            trace_id=result.trace_id,
            metadata=result.metadata,
        )