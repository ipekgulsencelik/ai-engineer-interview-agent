from __future__ import annotations

from datetime import datetime

from src.evaluation.runner.entities.runner_execution_result import (
    RunnerExecutionResult,
)


class RunnerExecutionResultFactory:
    """
    Factory for creating runner execution results.
    """

    def create_success(
        self,
        *,
        execution_id: str,
        runner_id: str,
        runner_name: str,
        started_at: datetime,
        completed_at: datetime,
        duration_ms: float,
        score: float | None,
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> RunnerExecutionResult:
        return RunnerExecutionResult(
            execution_id=execution_id,
            runner_id=runner_id,
            runner_name=runner_name,
            status="success",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            success=True,
            score=score,
            error_message=None,
            retry_count=0,
            output_uri=None,
            artifact_id=None,
            report_id=None,
            dataset_id=None,
            run_id=run_id,
            experiment_id=experiment_id,
            worker_id=worker_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )

    def create_failure(
        self,
        *,
        execution_id: str,
        runner_id: str,
        runner_name: str,
        started_at: datetime,
        completed_at: datetime,
        duration_ms: float,
        error_message: str,
        run_id: str | None = None,
        experiment_id: str | None = None,
        worker_id: str | None = None,
        correlation_id: str | None = None,
        trace_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> RunnerExecutionResult:
        return RunnerExecutionResult(
            execution_id=execution_id,
            runner_id=runner_id,
            runner_name=runner_name,
            status="failed",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            success=False,
            score=None,
            error_message=error_message,
            retry_count=0,
            output_uri=None,
            artifact_id=None,
            report_id=None,
            dataset_id=None,
            run_id=run_id,
            experiment_id=experiment_id,
            worker_id=worker_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            metadata=metadata,
        )