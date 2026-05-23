from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import UploadFile


class CVUploadFileStorage:
    """
    CV upload temporary file storage helper.
    """

    @staticmethod
    async def save_to_temp_file(
        *,
        file: UploadFile,
    ) -> Path:
        suffix = Path(
            file.filename or "",
        ).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            content = await file.read()

            if not content:
                raise ValueError(
                    "Uploaded CV file is empty."
                )

            temp_file.write(content)

            return Path(
                temp_file.name,
            )