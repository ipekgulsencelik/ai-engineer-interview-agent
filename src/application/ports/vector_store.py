from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.search.search_result import SearchResult


@runtime_checkable
class VectorStore(Protocol):
    
    @abstractmethod
    def add(
        self,
        *,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict[str, str],
     ) -> None:
        ...


    @abstractmethod
    def add_many(
        self,
        *,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, str]],
    ) -> None:
        ...


    @abstractmethod
    def search(
        self,
        *,
        query_embedding: list[float],
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        ...


    @abstractmethod
    def count(self) -> int:
        ...