from __future__ import annotations

from pathlib import Path
from typing import Protocol

from src.evaluation.reporting.entities.executive_summary import ExecutiveSummary
from src.evaluation.tracking.entities.experiment_comparison_result import ExperimentComparisonResult
from src.evaluation.tracking.entities.experiment_trend_result import ExperimentTrendResult


class TextReportWriter(Protocol):
    """Writes rendered text report content to a destination path."""

    def write(
        self,
        *,
        content: str,
        output_path: str | Path,
    ) -> Path: ...


class PDFReportWriter(Protocol):
    """Writes rendered HTML report content as a PDF."""

    def write(
        self,
        *,
        html: str,
        output_path: str | Path,
    ) -> Path: ...


class ExecutiveSummaryRenderer(Protocol):
    """Renders executive summaries into an export format."""

    def render(
        self,
        *,
        summary: ExecutiveSummary,
    ) -> str: ...


class ExperimentComparisonRenderer(Protocol):
    """Renders experiment comparisons into an export format."""

    def render(
        self,
        *,
        comparison: ExperimentComparisonResult,
    ) -> str: ...


class ExperimentTrendRenderer(Protocol):
    """Renders experiment trends into an export format."""

    def render(
        self,
        *,
        trend: ExperimentTrendResult,
    ) -> str: ...


class HTMLReportRenderer(Protocol):
    """Renders reporting payloads as HTML for downstream conversion."""

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
