from __future__ import annotations

from src.evaluation.runner.factories.runner_stream_event_factory import (
    RunnerStreamEventFactory,
)
from src.evaluation.reporting.streams.realtime_analytics_stream import (
    RealtimeAnalyticsStream,
)


class RunnerEventPublisher:
    """
    Publishes runner lifecycle events to realtime analytics stream.
    """

    def __init__(
        self,
        *,
        event_factory: RunnerStreamEventFactory,
        stream: RealtimeAnalyticsStream | None = None,
    ) -> None:
        self._event_factory = event_factory
        self._stream = stream

    def publish_started(
        self,
        *,
        execution_id: str,
        runner_id: str,
        runner_name: str,
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._publish(
            event_type="runner.started",
            execution_id=execution_id,
            sequence_number=0,
            payload={
                "runner_id": runner_id,
                "runner_name": runner_name,
                "status": "running",
            },
            runner_id=runner_id,
            runner_name=runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            worker_id=worker_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def publish_completed(
        self,
        *,
        execution_id: str,
        runner_id: str,
        runner_name: str,
        duration_ms: float,
        score: float | None,
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._publish(
            event_type="runner.completed",
            execution_id=execution_id,
            sequence_number=1,
            payload={
                "runner_id": runner_id,
                "runner_name": runner_name,
                "status": "success",
                "score": "" if score is None else str(score),
                "duration_ms": str(
                    duration_ms,
                ),
            },
            runner_id=runner_id,
            runner_name=runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            worker_id=worker_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def publish_failed(
        self,
        *,
        execution_id: str,
        runner_id: str,
        runner_name: str,
        duration_ms: float,
        error_message: str,
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._publish(
            event_type="runner.failed",
            execution_id=execution_id,
            sequence_number=1,
            payload={
                "runner_id": runner_id,
                "runner_name": runner_name,
                "status": "failed",
                "error_message": error_message,
                "duration_ms": str(
                    duration_ms,
                ),
            },
            runner_id=runner_id,
            runner_name=runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            worker_id=worker_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def _publish(
        self,
        *,
        event_type: str,
        execution_id: str,
        sequence_number: int,
        payload: dict[str, str],
        runner_id: str,
        runner_name: str,
        run_id: str | None,
        experiment_id: str | None,
        worker_id: str | None,
        correlation_id: str | None,
        trace_id: str | None,
        metadata: dict[str, str] | None,
    ) -> None:
        if self._stream is None:
            return

        self._stream.publish(
            event=self._event_factory.create(
                event_type=event_type,
                execution_id=execution_id,
                sequence_number=sequence_number,
                payload=payload,
                runner_id=runner_id,
                runner_name=runner_name,
                run_id=run_id,
                experiment_id=experiment_id,
                worker_id=worker_id,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )
        )