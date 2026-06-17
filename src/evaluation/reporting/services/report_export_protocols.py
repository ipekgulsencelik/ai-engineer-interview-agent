from __future__ import annotations

from pathlib import Path
from typing import Protocol

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.tracking.entities.experiment_comparison_result import (
    ExperimentComparisonResult,
)
from src.evaluation.tracking.entities.experiment_trend_result import (
    ExperimentTrendResult,
)


class TextReportExporter(Protocol):
    """Renders reporting payloads as text content."""

    def render_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
    ) -> str: ...

    def render_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
    ) -> str: ...

    def render_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> str: ...


class PDFReportExporter(Protocol):
    """Exports reporting payloads directly to PDF files."""

    def export_executive_summary(
        self,
        *,
        summary: ExecutiveSummary,
        output_path: Path,
    ) -> None: ...

    def export_experiment_comparison(
        self,
        *,
        comparison: ExperimentComparisonResult,
        output_path: Path,
    ) -> None: ...

    def export_experiment_trend(
        self,
        *,
        trend: ExperimentTrendResult,
        output_path: Path,
    ) -> None: ...


class ReportTextWriter(Protocol):
    """Writes rendered text report content."""

    def write_text(
        self,
        *,
        output_path: Path,
        content: str,
    ) -> None: ...
