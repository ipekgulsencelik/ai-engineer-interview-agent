from __future__ import annotations

from src.infrastructure.errors.chroma_client_error import (
    ChromaClientError,
)


class ChromaClientConfigValidator:
    """
    ChromaDB client configuration validator.
    """

    @staticmethod
    def validate_persist_directory(
        *,
        persist_directory: str,
    ) -> None:
        if not isinstance(persist_directory, str):
            raise ChromaClientError(
                "persist_directory must be a string."
            )

        if not persist_directory.strip():
            raise ChromaClientError(
                "persist_directory cannot be empty."
            )