from __future__ import annotations

from src.infrastructure.errors.chroma_collection_error import (
    ChromaCollectionError,
)


class ChromaCollectionConfigValidator:
    """
    Chroma collection configuration validator.
    """

    @staticmethod
    def validate_collection_name(
        *,
        collection_name: str,
    ) -> None:
        if not isinstance(collection_name, str):
            raise ChromaCollectionError(
                "collection_name must be a string."
            )

        if not collection_name.strip():
            raise ChromaCollectionError(
                "collection_name cannot be empty."
            )