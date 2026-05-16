from __future__ import annotations

from typing import Protocol


class ChromaCollectionProtocol(Protocol):
    def query(self, **kwargs: object) -> dict: ...
    def upsert(self, **kwargs: object) -> None: ...


class ChromaClientProtocol(Protocol):
    def get_or_create_collection(self, *, name: str) -> ChromaCollectionProtocol: ...