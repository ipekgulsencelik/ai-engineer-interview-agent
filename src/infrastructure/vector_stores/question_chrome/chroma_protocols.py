from __future__ import annotations

from typing import Any, Protocol


class ChromaCollectionProtocol(Protocol):
    def query(self, **kwargs: Any) -> dict: ...


class ChromaClientProtocol(Protocol):
    def get_or_create_collection(self, *, name: str) -> ChromaCollectionProtocol: ...