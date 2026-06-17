from __future__ import annotations

import inspect

import pytest

MODULE_UNDER_TEST = "src.evaluation.reporting.services.report_export_service"


def test_module_imports_and_exposes_public_api() -> None:
    module = pytest.importorskip(MODULE_UNDER_TEST, exc_type=ImportError)

    public_members = {
        name: value for name, value in vars(module).items() if not name.startswith("_")
    }

    assert public_members, "module should expose a public API"
    assert any(
        inspect.isclass(value) or inspect.isfunction(value) or name.isupper()
        for name, value in public_members.items()
    )


def test_public_callables_are_documented_or_named_explicitly() -> None:
    module = pytest.importorskip(MODULE_UNDER_TEST, exc_type=ImportError)

    public_callables = [
        value
        for name, value in vars(module).items()
        if not name.startswith("_")
        and (inspect.isclass(value) or inspect.isfunction(value))
        and getattr(value, "__module__", MODULE_UNDER_TEST) == MODULE_UNDER_TEST
    ]

    assert isinstance(public_callables, list)
    for value in public_callables:
        assert value.__name__


class _TextExporterStub:
    def __init__(self, content: str) -> None:
        self.content = content
        self.calls: list[tuple[str, object]] = []

    def render_executive_summary(self, *, summary) -> str:
        self.calls.append(("summary", summary))
        return self.content

    def render_experiment_comparison(self, *, comparison) -> str:
        self.calls.append(("comparison", comparison))
        return self.content

    def render_experiment_trend(self, *, trend) -> str:
        self.calls.append(("trend", trend))
        return self.content


class _PDFExporterStub:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object, object]] = []

    def export_executive_summary(self, *, summary, output_path) -> None:
        self.calls.append(("summary", summary, output_path))

    def export_experiment_comparison(self, *, comparison, output_path) -> None:
        self.calls.append(("comparison", comparison, output_path))

    def export_experiment_trend(self, *, trend, output_path) -> None:
        self.calls.append(("trend", trend, output_path))


class _ReportTextWriterStub:
    def __init__(self) -> None:
        self.writes: list[tuple[object, str]] = []

    def write_text(self, *, output_path, content: str) -> None:
        self.writes.append((output_path, content))


def _build_service(*, text_exporters=None):
    from src.evaluation.reporting.services.report_export_service import (
        ReportExportService,
    )

    markdown_exporter = _TextExporterStub("markdown-content")
    html_exporter = _TextExporterStub("html-content")
    json_exporter = _TextExporterStub("json-content")
    pdf_exporter = _PDFExporterStub()
    writer = _ReportTextWriterStub()

    service = ReportExportService(
        markdown_exporter=markdown_exporter,
        html_exporter=html_exporter,
        json_exporter=json_exporter,
        pdf_exporter=pdf_exporter,
        file_writer=writer,
        text_exporters=text_exporters,
    )

    return service, pdf_exporter, writer


def test_export_executive_summary_uses_injected_text_exporter(tmp_path) -> None:
    csv_exporter = _TextExporterStub("csv-content")
    service, pdf_exporter, writer = _build_service(
        text_exporters={
            "csv": csv_exporter,
        },
    )
    output_path = tmp_path / "summary.csv"
    summary = object()

    content = service.export_executive_summary(
        summary=summary,
        report_format="csv",
        output_path=output_path,
    )

    assert content == "csv-content"
    assert csv_exporter.calls == [("summary", summary)]
    assert writer.writes == [(output_path, "csv-content")]
    assert pdf_exporter.calls == []


def test_export_executive_summary_delegates_pdf_without_text_write(tmp_path) -> None:
    service, pdf_exporter, writer = _build_service()
    output_path = tmp_path / "summary.pdf"
    summary = object()

    content = service.export_executive_summary(
        summary=summary,
        report_format="pdf",
        output_path=output_path,
    )

    assert content is None
    assert pdf_exporter.calls == [("summary", summary, output_path)]
    assert writer.writes == []


def test_export_executive_summary_rejects_unknown_format(tmp_path) -> None:
    service, _pdf_exporter, writer = _build_service()

    with pytest.raises(ValueError, match="unsupported format: xml"):
        service.export_executive_summary(
            summary=object(),
            report_format="xml",
            output_path=tmp_path / "summary.xml",
        )

    assert writer.writes == []
