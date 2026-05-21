from __future__ import annotations

from typing import Any

from src.domain.retrieval.search_result import SearchResult
from src.infrastructure.constants.chroma_response_keys import (
    CHROMA_DISTANCES_KEY,
    CHROMA_DOCUMENTS_KEY,
    CHROMA_IDS_KEY,
    CHROMA_METADATAS_KEY,
)
from src.infrastructure.constants.retrieval_defaults import (
    DEFAULT_RETRIEVAL_CATEGORY,
    DEFAULT_RETRIEVAL_DIFFICULTY,
    DEFAULT_RETRIEVAL_LEVEL,
    DEFAULT_RETRIEVAL_QUESTION_TYPE,
    DEFAULT_RETRIEVAL_TEXT,
)
from src.infrastructure.constants.vector_metadata_keys import (
    CATEGORY_METADATA_KEY,
    DIFFICULTY_METADATA_KEY,
    LEVEL_METADATA_KEY,
    QUESTION_TYPE_METADATA_KEY,
)
from src.infrastructure.parsers.safe_int_parser import (
    SafeIntParser,
)
from src.infrastructure.parsers.safe_optional_float_parser import (
    SafeOptionalFloatParser,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    ChromaQueryResults,
)


class ChromaSearchResultMapper:
    """
    ChromaDB raw query result -> domain-safe SearchResult mapper.
    """

    @classmethod
    def to_results(
        cls,
        *,
        raw: ChromaQueryResults,
    ) -> list[SearchResult]:
        ids = cls._get_first_result_group(
            raw=raw,
            key=CHROMA_IDS_KEY,
        )

        if not ids:
            return []

        documents = cls._get_first_result_group(
            raw=raw,
            key=CHROMA_DOCUMENTS_KEY,
        )
        metadatas = cls._get_first_result_group(
            raw=raw,
            key=CHROMA_METADATAS_KEY,
        )
        distances = cls._get_first_result_group(
            raw=raw,
            key=CHROMA_DISTANCES_KEY,
        )

        results: list[SearchResult] = []

        for index, item_id in enumerate(ids):
            metadata = cls._get_metadata(
                metadatas=metadatas,
                index=index,
            )

            results.append(
                SearchResult(
                    id=str(item_id),
                    text=str(
                        cls._safe_get(
                            values=documents,
                            index=index,
                            default=DEFAULT_RETRIEVAL_TEXT,
                        )
                    ),
                    category=str(
                        metadata.get(
                            CATEGORY_METADATA_KEY,
                            DEFAULT_RETRIEVAL_CATEGORY,
                        )
                    ),
                    level=str(
                        metadata.get(
                            LEVEL_METADATA_KEY,
                            DEFAULT_RETRIEVAL_LEVEL,
                        )
                    ),
                    difficulty=SafeIntParser.parse(
                        value=metadata.get(
                            DIFFICULTY_METADATA_KEY,
                            DEFAULT_RETRIEVAL_DIFFICULTY,
                        ),
                        default=DEFAULT_RETRIEVAL_DIFFICULTY,
                    ),
                    question_type=str(
                        metadata.get(
                            QUESTION_TYPE_METADATA_KEY,
                            DEFAULT_RETRIEVAL_QUESTION_TYPE,
                        )
                    ),
                    distance=SafeOptionalFloatParser.parse(
                        value=cls._safe_get(
                            values=distances,
                            index=index,
                            default=None,
                        ),
                    ),
                )
            )

        return results

    @staticmethod
    def _get_first_result_group(
        *,
        raw: ChromaQueryResults,
        key: str,
    ) -> list[Any]:
        values = raw.get(key)

        if not values:
            return []

        if not isinstance(values, list):
            return []

        first_group = values[0]

        if not isinstance(first_group, list):
            return []

        return first_group

    @classmethod
    def _get_metadata(
        cls,
        *,
        metadatas: list[Any],
        index: int,
    ) -> dict[str, Any]:
        metadata = cls._safe_get(
            values=metadatas,
            index=index,
            default={},
        )

        if not isinstance(metadata, dict):
            return {}

        return metadata

    @staticmethod
    def _safe_get(
        *,
        values: list[Any],
        index: int,
        default: Any,
    ) -> Any:
        if index < 0:
            return default

        if index >= len(values):
            return default

        return values[index]