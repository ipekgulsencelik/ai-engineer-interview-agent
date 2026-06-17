from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.services.report_export_protocols import (
    PDFReportExporter,
    ReportTextWriter,
    TextReportExporter,
)
from src.evaluation.reporting.services.text_report_exporter_registry import (
    TextReportExporterRegistry,
)
from src.evaluation.tracking.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


PDF_REPORT_FORMAT = "pdf"


class ReportExportService:
    """
    Handles report rendering and file export operations.
    """

    def __init__(
        self,
        *,
        markdown_exporter: TextReportExporter,
        html_exporter: TextReportExporter,
        json_exporter: TextReportExporter,
        pdf_exporter: PDFReportExporter,
        file_writer: ReportTextWriter,
        text_exporters: Mapping[
            str,
            TextReportExporter,
        ]
        | None = None,
        text_exporter_registry: TextReportExporterRegistry | None = None,
    ) -> None:
        self._text_exporter_registry = (
            text_exporter_registry
            or TextReportExporterRegistry(
                markdown_exporter=markdown_exporter,
                html_exporter=html_exporter,
                json_exporter=json_exporter,
                text_exporters=text_exporters,
            )
        )
        self._pdf_exporter = pdf_exporter
        self._file_writer = file_writer

    def export_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
        report_format: str,
        output_path: Path,
    ) -> str | None:
        if report_format == PDF_REPORT_FORMAT:
            self._pdf_exporter.export_executive_summary(
                summary=summary,
                output_path=output_path,
            )
            return None

        exporter = self._text_exporter_registry.get(
            report_format=report_format,
        )
        content = exporter.render_executive_summary(
            summary=summary,
        )
        self._write_text(
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
        if report_format == PDF_REPORT_FORMAT:
            self._pdf_exporter.export_experiment_comparison(
                comparison=comparison,
                output_path=output_path,
            )
            return None

        exporter = self._text_exporter_registry.get(
            report_format=report_format,
        )
        content = exporter.render_experiment_comparison(
            comparison=comparison,
        )
        self._write_text(
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
        if report_format == PDF_REPORT_FORMAT:
            self._pdf_exporter.export_experiment_trend(
                trend=trend,
                output_path=output_path,
            )
            return None

        exporter = self._text_exporter_registry.get(
            report_format=report_format,
        )
        content = exporter.render_experiment_trend(
            trend=trend,
        )
        self._write_text(
            output_path=output_path,
            content=content,
        )

        return content

    def _write_text(
        self,
        *,
        output_path: Path,
        content: str,
    ) -> None:
        self._file_writer.write_text(
            output_path=output_path,
            content=content,
        )
