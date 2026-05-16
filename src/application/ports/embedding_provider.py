from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingProvider(Protocol):
    """
    Text embedding generation port.

    Application layer yalnızca bu contract'ı bilir.
    Concrete embedding provider infrastructure katmanında yer alır.
    """

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Single text embedding üretir.
        """
        ...

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Multiple text embedding üretir.
        """
        ...