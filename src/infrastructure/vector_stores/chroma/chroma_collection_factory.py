from __future__ import annotations

from src.infrastructure.errors.chroma_collection_error import (
    ChromaCollectionError,
)
from src.infrastructure.validators.chroma_collection_config_validator import (
    ChromaCollectionConfigValidator,
)
from src.infrastructure.vector_stores.chroma.chroma_protocols import (
    ChromaClientProtocol,
    ChromaCollectionProtocol,
)


def get_or_create_chroma_collection(
    *,
    client: ChromaClientProtocol,
    collection_name: str,
) -> ChromaCollectionProtocol:
    ChromaCollectionConfigValidator.validate_collection_name(
        collection_name=collection_name,
    )

    try:
        return client.get_or_create_collection(
            name=collection_name,
        )

    except Exception as exc:
        raise ChromaCollectionError(
            f"Failed to get or create Chroma collection: {collection_name}"
        ) from exc