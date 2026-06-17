from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.entities.report_artifact import (
    ReportArtifact,
)
from src.evaluation.reporting.factories.report_artifact_factory import (
    ReportArtifactFactory,
)
from src.evaluation.reporting.services.report_export_service import (
    ReportExportService,
)
from src.evaluation.reporting.builders.report_path_builder import (
    ReportPathBuilder,
)
from src.evaluation.tracking.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.tracking.value_objects.experiment_trend_result import (
    ExperimentTrendResult,
)


class ReportArtifactOrchestrator:
    """
    Orchestrates report export and report artifact creation.
    """

    def __init__(
        self,
        *,
        export_service: ReportExportService,
        artifact_factory: ReportArtifactFactory,
        path_builder: ReportPathBuilder,
    ) -> None:
        self._export_service = export_service
        self._artifact_factory = artifact_factory
        self._path_builder = path_builder

    def export_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
        run_id: str,
        experiment_id: str,
        output_directory: str | Path,
        report_format: str,
        generated_by: str | None = None,
    ) -> ReportArtifact:
        output_path = self._path_builder.build(
            output_directory=output_directory,
            filename=f"executive_summary_{summary.summary_id}",
            report_format=report_format,
        )

        content = self._export_service.export_executive_summary(
            summary=summary,
            report_format=report_format,
            output_path=output_path,
        )

        return self._artifact_factory.create(
            title=summary.title,
            report_type="executive_summary",
            run_id=run_id,
            experiment_id=experiment_id,
            report_format=report_format,
            output_path=output_path,
            content=content,
            generated_by=generated_by,
        )

    def export_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
        run_id: str,
        experiment_id: str,
        output_directory: str | Path,
        report_format: str,
        generated_by: str | None = None,
    ) -> ReportArtifact:
        output_path = self._path_builder.build(
            output_directory=output_directory,
            filename=(
                "experiment_comparison_"
                f"{comparison.candidate_run_id}"
            ),
            report_format=report_format,
        )

        content = self._export_service.export_experiment_comparison(
            comparison=comparison,
            report_format=report_format,
            output_path=output_path,
        )

        return self._artifact_factory.create(
            title="Experiment Comparison Report",
            report_type="experiment_comparison",
            run_id=run_id,
            experiment_id=experiment_id,
            report_format=report_format,
            output_path=output_path,
            content=content,
            generated_by=generated_by,
        )

    def export_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
        run_id: str,
        experiment_id: str,
        output_directory: str | Path,
        report_format: str,
        generated_by: str | None = None,
    ) -> ReportArtifact:
        output_path = self._path_builder.build(
            output_directory=output_directory,
            filename=f"experiment_trend_{trend.experiment_id}",
            report_format=report_format,
        )

        content = self._export_service.export_experiment_trend(
            trend=trend,
            report_format=report_format,
            output_path=output_path,
        )

        return self._artifact_factory.create(
            title="Experiment Trend Report",
            report_type="experiment_trend",
            run_id=run_id,
            experiment_id=experiment_id,
            report_format=report_format,
            output_path=output_path,
            content=content,
            generated_by=generated_by,
        )