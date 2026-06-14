from __future__ import annotations

from pathlib import Path


class HTMLFileWriter:
    """
    Writes HTML content to disk.
    """

    @staticmethod
    def write(
        *,
        content: str,
        output_path: str | Path,
    ) -> Path:
        path = Path(
            output_path,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path