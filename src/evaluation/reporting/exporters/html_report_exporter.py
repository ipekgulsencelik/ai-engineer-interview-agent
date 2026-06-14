from __future__ import annotations

from pathlib import Path

from src.evaluation.reporting.exporters.protocols import (
    ExecutiveSummaryRenderer,
    ExperimentComparisonRenderer,
    ExperimentTrendRenderer,
    TextReportWriter,
)
from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.renderers.executive_summary_html_renderer import (
    ExecutiveSummaryHTMLRenderer,
)
from src.evaluation.reporting.renderers.experiment_comparison_html_renderer import (
    ExperimentComparisonHTMLRenderer,
)
from src.evaluation.reporting.renderers.experiment_trend_html_renderer import (
    ExperimentTrendHTMLRenderer,
)
from src.evaluation.reporting.writers.html_file_writer import (
    HTMLFileWriter,
)
from src.evaluation.tracking.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class HTMLReportExporter:
    """
    Exports evaluation operations reports as HTML.
    """

    def __init__(
        self,
        *,
        file_writer: TextReportWriter | None = None,
        executive_summary_renderer: (
            ExecutiveSummaryRenderer | None
        ) = None,
        experiment_comparison_renderer: (
            ExperimentComparisonRenderer | None
        ) = None,
        experiment_trend_renderer: (
            ExperimentTrendRenderer | None
        ) = None,
    ) -> None:
        self._file_writer = (
            file_writer
            or HTMLFileWriter()
        )
        self._executive_summary_renderer = (
            executive_summary_renderer
            or ExecutiveSummaryHTMLRenderer()
        )
        self._experiment_comparison_renderer = (
            experiment_comparison_renderer
            or ExperimentComparisonHTMLRenderer()
        )
        self._experiment_trend_renderer = (
            experiment_trend_renderer
            or ExperimentTrendHTMLRenderer()
        )

    def export_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
        output_path: str | Path,
    ) -> Path:
        return self._file_writer.write(
            content=self.render_executive_summary(
                summary=summary,
            ),
            output_path=output_path,
        )

    def export_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
        output_path: str | Path,
    ) -> Path:
        return self._file_writer.write(
            content=self.render_experiment_comparison(
                comparison=comparison,
            ),
            output_path=output_path,
        )

    def export_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
        output_path: str | Path,
    ) -> Path:
        return self._file_writer.write(
            content=self.render_experiment_trend(
                trend=trend,
            ),
            output_path=output_path,
        )

    def render_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
    ) -> str:
        return self._executive_summary_renderer.render(
            summary=summary,
        )

    def render_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
    ) -> str:
        return self._experiment_comparison_renderer.render(
            comparison=comparison,
        )

    def render_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> str:
        return self._experiment_trend_renderer.render(
            trend=trend,
        )