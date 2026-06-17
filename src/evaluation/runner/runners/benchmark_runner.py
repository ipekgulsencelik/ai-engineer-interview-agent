from __future__ import annotations

from collections.abc import Callable
from datetime import UTC
from datetime import datetime
from time import perf_counter
from uuid import uuid4

from src.evaluation.runner.calculators.benchmark_pass_rate_calculator import (
    BenchmarkPassRateCalculator,
)
from src.evaluation.reporting.entities.telemetry_metric import (
    TelemetryMetric,
)
from src.evaluation.runner.factories.benchmark_result_factory import (
    BenchmarkResultFactory,
)
from src.evaluation.runner.services.benchmark_comparison_service import (
    BenchmarkComparisonService,
)
from src.evaluation.runner.publishers.benchmark_event_publisher import (
    BenchmarkEventPublisher,
)
from src.evaluation.runner.builders.benchmark_telemetry_builder import (
    BenchmarkTelemetryBuilder,
)
from src.evaluation.runner.entities.benchmark_result import (
    BenchmarkResult,
)


class BenchmarkRunner:
    """
    Executes benchmark workloads.
    """

    def __init__(
        self,
        *,
        runner_id: str,
        runner_name: str = "benchmark_runner",
        result_factory: BenchmarkResultFactory,
        event_publisher: BenchmarkEventPublisher,
        telemetry_builder: BenchmarkTelemetryBuilder,
        pass_rate_calculator: BenchmarkPassRateCalculator,
        comparison_service: BenchmarkComparisonService,
    ) -> None:
        self._runner_id = runner_id
        self._runner_name = runner_name
        self._result_factory = result_factory
        self._event_publisher = event_publisher
        self._telemetry_builder = telemetry_builder
        self._pass_rate_calculator = pass_rate_calculator
        self._comparison_service = comparison_service

    def run(
        self,
        *,
        workload: Callable[
            [],
            tuple[
                float,
                bool,
                int,
                int,
                int,
            ],
        ],
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        run_id: str,
        experiment_id: str,
        model_name: str,
        evaluator_name: str | None = None,
        dataset_id: str | None = None,
        dataset_name: str | None = None,
        dataset_version: str | None = None,
        tenant_id: str | None = None,
        baseline_run_id: str | None = None,
        candidate_run_id: str | None = None,
        baseline_score: float | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> BenchmarkResult:
        result_id = str(
            uuid4(),
        )

        started_at = datetime.now(
            UTC,
        )

        started_counter = perf_counter()

        self._event_publisher.publish_started(
            result_id=result_id,
            runner_id=self._runner_id,
            runner_name=self._runner_name,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            benchmark_version=benchmark_version,
            run_id=run_id,
            experiment_id=experiment_id,
            model_name=model_name,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

        try:
            (
                overall_score,
                passed,
                sample_count,
                passed_count,
                failed_count,
            ) = workload()

            completed_at = datetime.now(
                UTC,
            )

            duration_ms = (
                perf_counter()
                - started_counter
            ) * 1000

            pass_rate = self._pass_rate_calculator.calculate(
                sample_count=sample_count,
                passed_count=passed_count,
            )

            score_delta = self._comparison_service.score_delta(
                baseline_score=baseline_score,
                candidate_score=overall_score,
            )

            winner = self._comparison_service.winner(
                baseline_score=baseline_score,
                candidate_score=overall_score,
            )

            result = self._result_factory.create_success(
                result_id=result_id,
                benchmark_id=benchmark_id,
                benchmark_name=benchmark_name,
                benchmark_version=benchmark_version,
                run_id=run_id,
                experiment_id=experiment_id,
                model_name=model_name,
                started_at=started_at,
                completed_at=completed_at,
                overall_score=overall_score,
                passed=passed,
                sample_count=sample_count,
                passed_count=passed_count,
                failed_count=failed_count,
                duration_ms=duration_ms,
                pass_rate=pass_rate,
                evaluator_name=evaluator_name,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                dataset_version=dataset_version,
                tenant_id=tenant_id,
                baseline_run_id=baseline_run_id,
                candidate_run_id=candidate_run_id,
                score_delta=score_delta,
                winner=winner,
                metadata=metadata,
            )

            self._event_publisher.publish_completed(
                result_id=result_id,
                runner_id=self._runner_id,
                runner_name=self._runner_name,
                benchmark_id=benchmark_id,
                run_id=run_id,
                experiment_id=experiment_id,
                overall_score=overall_score,
                passed=passed,
                duration_ms=duration_ms,
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
                result_id=result_id,
                benchmark_id=benchmark_id,
                benchmark_name=benchmark_name,
                benchmark_version=benchmark_version,
                run_id=run_id,
                experiment_id=experiment_id,
                model_name=model_name,
                started_at=started_at,
                completed_at=completed_at,
                duration_ms=duration_ms,
                evaluator_name=evaluator_name,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                dataset_version=dataset_version,
                tenant_id=tenant_id,
                baseline_run_id=baseline_run_id,
                candidate_run_id=candidate_run_id,
                error_message=error_message,
                metadata=metadata,
            )

            self._event_publisher.publish_failed(
                result_id=result_id,
                runner_id=self._runner_id,
                runner_name=self._runner_name,
                benchmark_id=benchmark_id,
                run_id=run_id,
                experiment_id=experiment_id,
                error_message=error_message,
                duration_ms=duration_ms,
                correlation_id=correlation_id,
                trace_id=trace_id,
                metadata=metadata,
            )

            return result

    def telemetry_from_result(
        self,
        *,
        result: BenchmarkResult,
    ) -> tuple[
        TelemetryMetric,
        ...,
    ]:
        return self._telemetry_builder.build(
            result=result,
        )