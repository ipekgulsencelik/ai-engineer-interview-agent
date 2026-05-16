from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EnumValueNormalizer(Protocol):
    """
    Raw enum string normalization contract.
    """

    def normalize(
        self,
        *,
        value: str,
    ) -> str:
        ...