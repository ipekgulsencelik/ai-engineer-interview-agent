from __future__ import annotations

from collections.abc import Mapping

from src.evaluation.reporting.services.report_export_protocols import (
    TextReportExporter,
)


DEFAULT_TEXT_EXPORTER_FORMATS = (
    "markdown",
    "html",
    "json",
)


class TextReportExporterRegistry:
    """Resolves text report exporters by report format."""

    def __init__(
        self,
        *,
        markdown_exporter: TextReportExporter,
        html_exporter: TextReportExporter,
        json_exporter: TextReportExporter,
        text_exporters: Mapping[
            str,
            TextReportExporter,
        ]
        | None = None,
    ) -> None:
        self._text_exporters = dict(
            text_exporters
            or zip(
                DEFAULT_TEXT_EXPORTER_FORMATS,
                (
                    markdown_exporter,
                    html_exporter,
                    json_exporter,
                ),
                strict=True,
            )
        )

    def get(
        self,
        *,
        report_format: str,
    ) -> TextReportExporter:
        try:
            return self._text_exporters[report_format]
        except KeyError as exc:
            raise ValueError(
                f"unsupported format: {report_format}",
            ) from exc
