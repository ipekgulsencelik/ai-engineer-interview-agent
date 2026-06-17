from __future__ import annotations

from src.evaluation.runner.factories.benchmark_stream_event_factory import (
    BenchmarkStreamEventFactory,
)
from src.evaluation.reporting.streams.realtime_analytics_stream import (
    RealtimeAnalyticsStream,
)


class BenchmarkEventPublisher:
    """
    Publishes benchmark lifecycle events.
    """

    def __init__(
        self,
        *,
        event_factory: BenchmarkStreamEventFactory,
        stream: RealtimeAnalyticsStream | None = None,
    ) -> None:
        self._event_factory = event_factory
        self._stream = stream

    def publish_started(
        self,
        *,
        result_id: str,
        runner_id: str,
        runner_name: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        run_id: str,
        experiment_id: str,
        model_name: str,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._publish(
            event_type="benchmark.started",
            result_id=result_id,
            sequence_number=0,
            payload={
                "runner_id": runner_id,
                "runner_name": runner_name,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "run_id": run_id,
                "experiment_id": experiment_id,
                "model_name": model_name,
                "status": "running",
            },
            runner_name=runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def publish_completed(
        self,
        *,
        result_id: str,
        runner_id: str,
        runner_name: str,
        benchmark_id: str,
        run_id: str,
        experiment_id: str,
        overall_score: float,
        passed: bool,
        duration_ms: float,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._publish(
            event_type="benchmark.completed",
            result_id=result_id,
            sequence_number=1,
            payload={
                "runner_id": runner_id,
                "runner_name": runner_name,
                "benchmark_id": benchmark_id,
                "run_id": run_id,
                "status": "success",
                "overall_score": str(
                    overall_score,
                ),
                "passed": str(
                    passed,
                ),
                "duration_ms": str(
                    duration_ms,
                ),
            },
            runner_name=runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def publish_failed(
        self,
        *,
        result_id: str,
        runner_id: str,
        runner_name: str,
        benchmark_id: str,
        run_id: str,
        experiment_id: str,
        error_message: str,
        duration_ms: float,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._publish(
            event_type="benchmark.failed",
            result_id=result_id,
            sequence_number=1,
            payload={
                "runner_id": runner_id,
                "runner_name": runner_name,
                "benchmark_id": benchmark_id,
                "run_id": run_id,
                "status": "failed",
                "error_message": error_message,
                "duration_ms": str(
                    duration_ms,
                ),
            },
            runner_name=runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def _publish(
        self,
        *,
        event_type: str,
        result_id: str,
        sequence_number: int,
        payload: dict[str, str],
        runner_name: str,
        run_id: str,
        experiment_id: str,
        correlation_id: str | None,
        trace_id: str | None,
        metadata: dict[str, str] | None,
    ) -> None:
        if self._stream is None:
            return

        self._stream.publish(
            event=self._event_factory.create(
                event_type=event_type,
                result_id=result_id,
                sequence_number=sequence_number,
                payload=payload,
                runner_name=runner_name,
                run_id=run_id,
                experiment_id=experiment_id,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )
        )