from __future__ import annotations

from pathlib import Path


class ReportPathBuilder:
    """
    Builds filesystem paths for generated reports.
    """

    def build(
        self,
        *,
        output_directory: str | Path,
        filename: str,
        report_format: str,
    ) -> Path:
        directory = Path(
            output_directory,
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory / f"{filename}.{report_format}"