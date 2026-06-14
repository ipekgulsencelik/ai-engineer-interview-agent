from __future__ import annotations

from pathlib import Path

from src.evaluation.ops.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.ops.exporters.executive_summary_json_renderer import (
    ExecutiveSummaryJSONRenderer,
)
from src.evaluation.ops.exporters.experiment_comparison_json_renderer import (
    ExperimentComparisonJSONRenderer,
)
from src.evaluation.ops.exporters.experiment_trend_json_renderer import (
    ExperimentTrendJSONRenderer,
)
from src.evaluation.ops.exporters.json_file_writer import (
    JSONFileWriter,
)
from src.evaluation.ops.value_objects.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.ops.value_objects.experiment_trend_result import (
    ExperimentTrendResult,
)


class JSONReportExporter:
    """
    Exports evaluation operations reports as JSON.
    """

    def __init__(
        self,
        *,
        file_writer: JSONFileWriter | None = None,
        executive_summary_renderer: (
            ExecutiveSummaryJSONRenderer | None
        ) = None,
        experiment_comparison_renderer: (
            ExperimentComparisonJSONRenderer | None
        ) = None,
        experiment_trend_renderer: (
            ExperimentTrendJSONRenderer | None
        ) = None,
    ) -> None:
        self._file_writer = (
            file_writer
            or JSONFileWriter()
        )
        self._executive_summary_renderer = (
            executive_summary_renderer
            or ExecutiveSummaryJSONRenderer()
        )
        self._experiment_comparison_renderer = (
            experiment_comparison_renderer
            or ExperimentComparisonJSONRenderer()
        )
        self._experiment_trend_renderer = (
            experiment_trend_renderer
            or ExperimentTrendJSONRenderer()
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