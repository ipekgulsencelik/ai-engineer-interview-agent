from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.entities.scheduled_report import (
    ScheduledReport,
)
from src.evaluation.reporting.orchestrators.report_artifact_orchestrator import (
    ReportArtifactOrchestrator,
)
from src.evaluation.reporting.services.scheduled_report_state_service import (
    ScheduledReportStateService,
)


class ScheduledReportRunner:
    """
    Runs a single scheduled report and updates schedule state.
    """

    def __init__(
        self,
        *,
        report_orchestrator: ReportArtifactOrchestrator,
        state_service: ScheduledReportStateService,
    ) -> None:
        self._report_orchestrator = report_orchestrator
        self._state_service = state_service

    def run(
        self,
        *,
        scheduled_report: ScheduledReport,
        summaries: dict[
            str,
            ExecutiveSummary,
        ],
        now: datetime,
    ) -> ReportArtifact:
        summary = summaries.get(
            scheduled_report.report_id,
        )

        if summary is None:
            error = (
                "executive summary not found "
                f"for report_id={scheduled_report.report_id}"
            )

            self._state_service.mark_failure(
                scheduled_report=scheduled_report,
                now=now,
                error=error,
            )

            raise EvaluationValidationError(
                error,
            )

        try:
            artifact = (
                self._report_orchestrator.export_executive_summary(
                    summary=summary,
                    run_id=(
                        scheduled_report.run_id
                        or "scheduled"
                    ),
                    experiment_id=(
                        scheduled_report.experiment_id
                        or "scheduled"
                    ),
                    output_directory=Path(
                        scheduled_report.output_directory,
                    ),
                    report_format=scheduled_report.report_format,
                    generated_by=scheduled_report.generated_by,
                )
            )

            self._state_service.mark_success(
                scheduled_report=scheduled_report,
                now=now,
            )

            return artifact

        except Exception as exc:
            self._state_service.mark_failure(
                scheduled_report=scheduled_report,
                now=now,
                error=str(
                    exc,
                ),
            )

            raise