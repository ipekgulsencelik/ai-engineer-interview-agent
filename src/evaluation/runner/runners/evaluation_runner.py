from __future__ import annotations

from collections.abc import Callable
from datetime import UTC
from datetime import datetime
from time import perf_counter
from uuid import uuid4

from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.runner.factories.runner_execution_result_factory import (
    RunnerExecutionResultFactory,
)
from src.evaluation.runner.publishers.runner_event_publisher import (
    RunnerEventPublisher,
)
from src.evaluation.runner.builders.runner_telemetry_builder import (
    RunnerTelemetryBuilder,
)
from src.evaluation.runner.entities.runner_execution_result import (
    RunnerExecutionResult,
)


class EvaluationRunner:
    """
    Executes evaluation workloads and coordinates result,
    event, and telemetry generation.
    """

    def __init__(
        self,
        *,
        runner_id: str,
        runner_name: str = "evaluation_runner",
        result_factory: RunnerExecutionResultFactory,
        event_publisher: RunnerEventPublisher,
        telemetry_builder: RunnerTelemetryBuilder,
    ) -> None:
        self._runner_id = runner_id
        self._runner_name = runner_name
        self._result_factory = result_factory
        self._event_publisher = event_publisher
        self._telemetry_builder = telemetry_builder

    def run(
        self,
        *,
        workload: Callable[
            [],
            float | None,
        ],
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> RunnerExecutionResult:
        execution_id = str(
            uuid4(),
        )

        started_at = datetime.now(
            UTC,
        )

        started_counter = perf_counter()

        self._event_publisher.publish_started(
            execution_id=execution_id,
            runner_id=self._runner_id,
            runner_name=self._runner_name,
            run_id=run_id,
            experiment_id=experiment_id,
            worker_id=worker_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

        try:
            score = workload()

            completed_at = datetime.now(
                UTC,
            )

            duration_ms = (
                perf_counter()
                - started_counter
            ) * 1000

            result = self._result_factory.create_success(
                execution_id=execution_id,
                runner_id=self._runner_id,
                runner_name=self._runner_name,
                started_at=started_at,
                completed_at=completed_at,
                duration_ms=duration_ms,
                score=score,
                run_id=run_id,
                experiment_id=experiment_id,
                worker_id=worker_id,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )

            self._event_publisher.publish_completed(
                execution_id=execution_id,
                runner_id=self._runner_id,
                runner_name=self._runner_name,
                duration_ms=duration_ms,
                score=score,
                run_id=run_id,
                experiment_id=experiment_id,
                worker_id=worker_id,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )

            return result

        except Exception as exc:
            completed_at = datetime.now(
                UTC,
            )

            duration_ms = (
                perf_counter()
                - started_counter
            ) * 1000

            error_message = str(
                exc,
            )

            result = self._result_factory.create_failure(
                execution_id=execution_id,
                runner_id=self._runner_id,
                runner_name=self._runner_name,
                started_at=started_at,
                completed_at=completed_at,
                duration_ms=duration_ms,
                error_message=error_message,
                run_id=run_id,
                experiment_id=experiment_id,
                worker_id=worker_id,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )

            self._event_publisher.publish_failed(
                execution_id=execution_id,
                runner_id=self._runner_id,
                runner_name=self._runner_name,
                duration_ms=duration_ms,
                error_message=error_message,
                run_id=run_id,
                experiment_id=experiment_id,
                worker_id=worker_id,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )

            return result

    def telemetry_from_result(
        self,
        *,
        result: RunnerExecutionResult,
        tenant_id: str | None = None,
    ) -> tuple[
        TelemetryMetric,
        ...,
    ]:
        return self._telemetry_builder.build(
            result=result,
            tenant_id=tenant_id,
        )