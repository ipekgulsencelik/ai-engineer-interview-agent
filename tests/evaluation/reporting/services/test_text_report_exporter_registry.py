from __future__ import annotations

import pytest

from src.evaluation.reporting.services.text_report_exporter_registry import (
    TextReportExporterRegistry,
)


class _TextExporterStub:
    def render_executive_summary(self, *, summary) -> str:
        return "summary"

    def render_experiment_comparison(self, *, comparison) -> str:
        return "comparison"

    def render_experiment_trend(self, *, trend) -> str:
        return "trend"


def test_registry_resolves_default_text_exporters_by_format() -> None:
    markdown_exporter = _TextExporterStub()
    html_exporter = _TextExporterStub()
    json_exporter = _TextExporterStub()

    registry = TextReportExporterRegistry(
        markdown_exporter=markdown_exporter,
        html_exporter=html_exporter,
        json_exporter=json_exporter,
    )

    assert registry.get(report_format="markdown") is markdown_exporter
    assert registry.get(report_format="html") is html_exporter
    assert registry.get(report_format="json") is json_exporter


def test_registry_accepts_custom_text_exporters() -> None:
    custom_exporter = _TextExporterStub()
    fallback_exporter = _TextExporterStub()

    registry = TextReportExporterRegistry(
        markdown_exporter=fallback_exporter,
        html_exporter=fallback_exporter,
        json_exporter=fallback_exporter,
        text_exporters={
            "csv": custom_exporter,
        },
    )

    assert registry.get(report_format="csv") is custom_exporter


def test_registry_rejects_unknown_format() -> None:
    exporter = _TextExporterStub()
    registry = TextReportExporterRegistry(
        markdown_exporter=exporter,
        html_exporter=exporter,
        json_exporter=exporter,
    )

    with pytest.raises(ValueError, match="unsupported format: xml"):
        registry.get(report_format="xml")
