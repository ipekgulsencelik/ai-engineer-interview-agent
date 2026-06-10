from __future__ import annotations

from abc import abstractmethod
from typing import Any, Protocol, runtime_checkable

from src.domain.search.search_result import SearchResult


@runtime_checkable
class VectorStore(Protocol):
    """
    Generic vector store port.
    """

    @abstractmethod
    def add(
        self,
        *,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict[str, Any],
    ) -> None:
        """Persist a generic vector record."""
        ...


    @abstractmethod
    def add_many(
        self,
        *,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        ...


    @abstractmethod
    def search(
        self,
        *,
        query_embedding: list[float],
        limit: int = 5,
        where: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        ...


    @abstractmethod
    def count(self) -> int:
        ...