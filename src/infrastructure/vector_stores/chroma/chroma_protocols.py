from __future__ import annotations

from typing import Any, Protocol


class ChromaCollectionProtocol(Protocol):
    """
    Minimal Chroma collection contract used by infrastructure adapters.
    """

    def query(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        ...

    def upsert(
        self,
        **kwargs: Any,
    ) -> None:
        ...


class ChromaClientProtocol(Protocol):
    """
    Minimal Chroma client contract used by collection factories.
    """

    def get_or_create_collection(
        self,
        *,
        name: str,
    ) -> ChromaCollectionProtocol:
        ...