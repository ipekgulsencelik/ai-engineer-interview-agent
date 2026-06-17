from __future__ import annotations

import importlib


def test_report_export_protocols_module_exposes_protocol_contracts() -> None:
    module = importlib.import_module(
        "src.evaluation.reporting.services.report_export_protocols"
    )

    assert module.TextReportExporter.__name__ == "TextReportExporter"
    assert module.PDFReportExporter.__name__ == "PDFReportExporter"
    assert module.ReportTextWriter.__name__ == "ReportTextWriter"
