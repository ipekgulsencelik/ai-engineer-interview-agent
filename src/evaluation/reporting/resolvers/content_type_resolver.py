from __future__ import annotations


class ContentTypeResolver:
    """
    Resolves MIME content types for report formats.
    """

    _CONTENT_TYPES: dict[str, str] = {
        "markdown": "text/markdown",
        "html": "text/html",
        "json": "application/json",
        "pdf": "application/pdf",
    }

    def resolve(
        self,
        *,
        report_format: str,
    ) -> str:
        return self._CONTENT_TYPES.get(
            report_format,
            "application/octet-stream",
        )