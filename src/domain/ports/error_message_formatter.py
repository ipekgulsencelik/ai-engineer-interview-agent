from __future__ import annotations

from typing import Protocol


class ErrorMessageFormatter(Protocol):
    """
    Error message formatter contract.

    Concrete formatter sınıflarının ortak davranışını tanımlar.
    """

    def format(self) -> str:
        """
        Error message string çıktısı üretir.
        """
        ...