from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile


class TemporaryHTMLFileFactory:
    """
    Creates temporary HTML files.
    """

    @staticmethod
    def create(
        *,
        html: str,
    ) -> Path:
        with NamedTemporaryFile(
            mode="w",
            suffix=".html",
            encoding="utf-8",
            delete=False,
        ) as temporary_file:
            temporary_file.write(
                html,
            )

            return Path(
                temporary_file.name,
            )