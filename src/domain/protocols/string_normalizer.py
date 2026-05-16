from __future__ import annotations

from typing import Protocol


class StringNormalizer(Protocol):
    """
    String normalization contract.
    """

    def normalize(
        self,
        value: str,
    ) -> str: ...
