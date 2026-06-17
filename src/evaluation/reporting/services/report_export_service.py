from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.exporters.html_report_exporter import (
    HTMLReportExporter,
)
from src.evaluation.reporting.exporters.json_report_exporter import (
    JSONReportExporter,
)
from src.evaluation.reporting.exporters.markdown_report_exporter import (
    MarkdownReportExporter,
)
from src.evaluation.reporting.exporters.pdf_report_exporter import (
    PDFReportExporter,
)
from src.evaluation.reporting.services.report_file_writer import (
    ReportFileWriter,
)
from src.evaluation.reporting.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.reporting.value_objects.experiment_trend_result import (
    ExperimentTrendResult,
)


class ReportExportService:
    """
    Handles report rendering and file export operations.
    """

    def __init__(
        self,
        *,
        markdown_exporter: MarkdownReportExporter,
        html_exporter: HTMLReportExporter,
        json_exporter: JSONReportExporter,
        pdf_exporter: PDFReportExporter,
        file_writer: ReportFileWriter,
    ) -> None:
        self._markdown_exporter = markdown_exporter
        self._html_exporter = html_exporter
        self._json_exporter = json_exporter
        self._pdf_exporter = pdf_exporter
        self._file_writer = file_writer

    def export_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
        report_format: str,
        output_path: Path,
    ) -> str | None:
        match report_format:
            case "markdown":
                content = (
                    self._markdown_exporter.render_executive_summary(
                        summary=summary,
                    )
                )

            case "html":
                content = (
                    self._html_exporter.render_executive_summary(
                        summary=summary,
                    )
                )

            case "json":
                content = (
                    self._json_exporter.render_executive_summary(
                        summary=summary,
                    )
                )

            case "pdf":
                self._pdf_exporter.export_executive_summary(
                    summary=summary,
                    output_path=output_path,
                )
                return None

            case _:
                raise ValueError(
                    f"unsupported format: {report_format}",
                )

        self._file_writer.write_text(
            output_path=output_path,
            content=content,
        )

        return content

    def export_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
        report_format: str,
        output_path: Path,
    ) -> str | None:
        match report_format:
            case "markdown":
                content = (
                    self._markdown_exporter.render_experiment_comparison(
                        comparison=comparison,
                    )
                )

            case "html":
                content = (
                    self._html_exporter.render_experiment_comparison(
                        comparison=comparison,
                    )
                )

            case "json":
                content = (
                    self._json_exporter.render_experiment_comparison(
                        comparison=comparison,
                    )
                )

            case "pdf":
                self._pdf_exporter.export_experiment_comparison(
                    comparison=comparison,
                    output_path=output_path,
                )
                return None

            case _:
                raise ValueError(
                    f"unsupported format: {report_format}",
                )

        self._file_writer.write_text(
            output_path=output_path,
            content=content,
        )

        return content

    def export_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
        report_format: str,
        output_path: Path,
    ) -> str | None:
        match report_format:
            case "markdown":
                content = (
                    self._markdown_exporter.render_experiment_trend(
                        trend=trend,
                    )
                )

            case "html":
                content = (
                    self._html_exporter.render_experiment_trend(
                        trend=trend,
                    )
                )

            case "json":
                content = (
                    self._json_exporter.render_experiment_trend(
                        trend=trend,
                    )
                )

            case "pdf":
                self._pdf_exporter.export_experiment_trend(
                    trend=trend,
                    output_path=output_path,
                )
                return None

            case _:
                raise ValueError(
                    f"unsupported format: {report_format}",
                )

        self._file_writer.write_text(
            output_path=output_path,
            content=content,
        )

        return content