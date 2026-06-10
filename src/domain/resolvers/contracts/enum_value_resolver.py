from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EnumValueResolver(Protocol):
    """
    Normalized enum value resolver contract.
    """

    def resolve(
        self,
        *,
        value: str,
    ) -> str:
        ...