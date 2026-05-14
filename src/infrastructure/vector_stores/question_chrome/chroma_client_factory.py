from __future__ import annotations

import chromadb

from src.infrastructure.vector_stores.question_chroma.chroma_protocols import (
    ChromaClientProtocol,
)


def create_chroma_client(*, persist_directory: str) -> ChromaClientProtocol:
    return chromadb.PersistentClient(path=persist_directory)