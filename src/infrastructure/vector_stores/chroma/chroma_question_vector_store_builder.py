from __future__ import annotations

from src.infrastructure.constants.chroma_defaults import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
)
from src.infrastructure.vector_stores.chroma.chroma_client_factory import (
    create_chroma_client,
)
from src.infrastructure.vector_stores.chroma.chroma_collection_factory import (
    get_or_create_chroma_collection,
)
from src.infrastructure.vector_stores.chroma.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)


class ChromaQuestionVectorStoreBuilder:
    """
    ChromaQuestionVectorStore dependency composition builder.
    """

    @staticmethod
    def build_default(
        *,
        persist_directory: str = DEFAULT_CHROMA_PERSIST_DIRECTORY,
        collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    ) -> ChromaQuestionVectorStore:
        client = create_chroma_client(
            persist_directory=persist_directory,
        )

        collection = get_or_create_chroma_collection(
            client=client,
            collection_name=collection_name,
        )

        return ChromaQuestionVectorStore(
            collection=collection,
        )