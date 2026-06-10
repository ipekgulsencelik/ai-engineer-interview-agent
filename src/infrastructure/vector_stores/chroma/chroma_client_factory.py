from __future__ import annotations

import chromadb

from src.infrastructure.errors.chroma_client_error import (
    ChromaClientError,
)
from src.infrastructure.validators.chroma_client_config_validator import (
    ChromaClientConfigValidator,
)
from src.infrastructure.vector_stores.chroma.chroma_protocols import (
    ChromaClientProtocol,
)


def create_chroma_client(
    *,
    persist_directory: str,
) -> ChromaClientProtocol:
    ChromaClientConfigValidator.validate_persist_directory(
        persist_directory=persist_directory,
    )

    try:
        return chromadb.PersistentClient(
            path=persist_directory,
        )

    except Exception as exc:
        raise ChromaClientError(
            "Failed to create Chroma persistent client."
        ) from exc