from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.entities.scheduled_report import (
    ScheduledReport,
)
from src.evaluation.reporting.schedulers.scheduled_report_due_checker import (
    ScheduledReportDueChecker,
)
from src.evaluation.reporting.services.scheduled_report_runner import (
    ScheduledReportRunner,
)
from src.evaluation.reporting.stores.scheduled_report_store import (
    ScheduledReportStore,
)


class ReportScheduler:
    """
    Coordinates scheduled report execution.
    """

    def __init__(
        self,
        *,
        store: ScheduledReportStore,
        due_checker: ScheduledReportDueChecker,
        runner: ScheduledReportRunner,
    ) -> None:
        self._store = store
        self._due_checker = due_checker
        self._runner = runner

    def run_due_reports(
        self,
        *,
        summaries: dict[
            str,
            ExecutiveSummary,
        ],
        now: datetime | None = None,
    ) -> tuple[
        ReportArtifact,
        ...,
    ]:
        current_time = now or datetime.now(
            UTC,
        )

        artifacts: list[
            ReportArtifact
        ] = []

        for scheduled_report in self._store.list_enabled():
            if not self._due_checker.is_due(
                scheduled_report=scheduled_report,
                now=current_time,
            ):
                continue

            artifact = self._runner.run(
                scheduled_report=scheduled_report,
                summaries=summaries,
                now=current_time,
            )

            artifacts.append(
                artifact,
            )

        return tuple(
            artifacts,
        )

    def run_once(
        self,
        *,
        scheduled_report: ScheduledReport,
        summaries: dict[
            str,
            ExecutiveSummary,
        ],
        now: datetime | None = None,
    ) -> ReportArtifact:
        return self._runner.run(
            scheduled_report=scheduled_report,
            summaries=summaries,
            now=now
            or datetime.now(
                UTC,
            ),
        )