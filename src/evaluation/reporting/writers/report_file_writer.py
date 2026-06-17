from __future__ import annotations

from pathlib import Path


class ReportFileWriter:
    """
    Writes report content to disk.
    """

    def write_text(
        self,
        *,
        output_path: Path,
        content: str,
    ) -> None:
        output_path.write_text(
            content,
            encoding="utf-8",
        )