from __future__ import annotations

from pathlib import Path

from src.evaluation.ops.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.ops.exporters.html_report_exporter import (
    HTMLReportExporter,
)
from src.evaluation.ops.exporters.pdf_writer import (
    PDFWriter,
)
from src.evaluation.ops.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.ops.value_objects.experiment_trend_result import (
    ExperimentTrendResult,
)


class PDFReportExporter:
    """
    Exports evaluation operation reports as PDF.
    """

    def __init__(
        self,
        *,
        html_exporter: (
            HTMLReportExporter | None
        ) = None,
        pdf_writer: PDFWriter | None = None,
    ) -> None:
        self._html_exporter = (
            html_exporter
            or HTMLReportExporter()
        )

        self._pdf_writer = (
            pdf_writer
            or PDFWriter()
        )

    def export_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
        output_path: str | Path,
    ) -> Path:
        html = (
            self._html_exporter.render_executive_summary(
                summary=summary,
            )
        )

        return self._pdf_writer.write(
            html=html,
            output_path=output_path,
        )

    def export_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
        output_path: str | Path,
    ) -> Path:
        html = (
            self._html_exporter.render_experiment_comparison(
                comparison=comparison,
            )
        )

        return self._pdf_writer.write(
            html=html,
            output_path=output_path,
        )

    def export_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
        output_path: str | Path,
    ) -> Path:
        html = (
            self._html_exporter.render_experiment_trend(
                trend=trend,
            )
        )

        return self._pdf_writer.write(
            html=html,
            output_path=output_path,
        )