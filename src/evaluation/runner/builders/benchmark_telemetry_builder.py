from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.runner.entities.benchmark_result import (
    BenchmarkResult,
)


class BenchmarkTelemetryBuilder:
    """
    Builds telemetry metrics from benchmark results.
    """

    def __init__(
        self,
        *,
        runner_id: str,
        runner_name: str,
    ) -> None:
        self._runner_id = runner_id
        self._runner_name = runner_name

    def build(
        self,
        *,
        result: BenchmarkResult,
    ) -> tuple[
        TelemetryMetric,
        ...,
    ]:
        recorded_at = result.completed_at

        labels = self._labels(
            result=result,
        )

        metrics = [
            self._metric(
                name="benchmark.overall_score",
                value=result.overall_score,
                unit="score",
                recorded_at=recorded_at,
                labels=labels,
                result=result,
            ),
            self._metric(
                name="benchmark.pass_rate",
                value=(
                    result.pass_rate
                    if result.pass_rate is not None
                    else result.calculated_pass_rate
                ),
                unit="ratio",
                recorded_at=recorded_at,
                labels=labels,
                result=result,
            ),
            self._metric(
                name="benchmark.sample_count",
                value=float(
                    result.sample_count,
                ),
                unit="count",
                recorded_at=recorded_at,
                labels=labels,
                result=result,
            ),
        ]

        if result.duration_ms is not None:
            metrics.append(
                self._metric(
                    name="benchmark.duration_ms",
                    value=result.duration_ms,
                    unit="ms",
                    recorded_at=recorded_at,
                    labels=labels,
                    result=result,
                )
            )

        if result.score_delta is not None:
            metrics.append(
                self._metric(
                    name="benchmark.score_delta",
                    value=result.score_delta,
                    unit="score",
                    recorded_at=recorded_at,
                    labels={
                        **labels,
                        "winner": result.winner or "",
                    },
                    result=result,
                )
            )

        return tuple(
            metrics,
        )

    def _labels(
        self,
        *,
        result: BenchmarkResult,
    ) -> dict[str, str]:
        return {
            "runner_id": self._runner_id,
            "runner_name": self._runner_name,
            "benchmark_id": result.benchmark_id,
            "benchmark_name": result.benchmark_name,
            "benchmark_version": result.benchmark_version,
            "model_name": result.model_name,
            "passed": str(
                result.passed,
            ),
        }

    def _metric(
        self,
        *,
        name: str,
        value: float,
        unit: str,
        recorded_at: datetime,
        labels: dict[str, str],
        result: BenchmarkResult,
    ) -> TelemetryMetric:
        return TelemetryMetric(
            metric_id=str(
                uuid4(),
            ),
            metric_name=name,
            metric_value=value,
            unit=unit,
            source=self._runner_name,
            recorded_at=recorded_at,
            labels=labels,
            tenant_id=result.tenant_id,
            experiment_id=result.experiment_id,
            run_id=result.run_id,
            metadata=result.metadata,
        )