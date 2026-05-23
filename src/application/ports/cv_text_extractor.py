from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class CVTextExtractor(Protocol):
    """
    Provider-independent CV text extraction contract.

    Bu protocol:
        - infrastructure extractor implementasyonlarını soyutlar
        - structural typing sağlar
        - application katmanını concrete dependency'lerden izole eder
    """

    def extract_text(
        self,
        file_path: str | Path,
    ) -> str:
        """
        CV dosyasından raw text çıkarır.
        """