from __future__ import annotations

from typing import Any

from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)
from src.infrastructure.constants.chroma_response_keys import (
    CHROMA_DISTANCES_KEY,
    CHROMA_IDS_KEY,
    CHROMA_METADATAS_KEY,
)
from src.infrastructure.constants.retrieval_defaults import (
    DEFAULT_RETRIEVAL_DISTANCE,
)
from src.infrastructure.errors.vector_store_error import (
    VectorStoreError,
)
from src.infrastructure.mappers.chroma_question_result_mapper import (
    ChromaQuestionResultMapper,
)
from src.infrastructure.scorers.distance_score_converter import (
    DistanceScoreConverter,
)
from src.infrastructure.vector_stores.chroma.chroma_question_types import (
    ChromaQueryResults,
    ChromaQuestionMetadata,
)


class ChromaQuestionSearchResultMapper:
    """
    Chroma query response -> QuestionSearchResult mapper.
    """

    def __init__(
        self,
        *,
        question_mapper: ChromaQuestionResultMapper | None = None,
    ) -> None:
        self._question_mapper = (
            question_mapper
            or ChromaQuestionResultMapper()
        )

    def to_results(
        self,
        *,
        results: ChromaQueryResults,
    ) -> list[QuestionSearchResult]:
        ids = self._get_first_group(
            results=results,
            key=CHROMA_IDS_KEY,
        )

        if not ids:
            return []

        metadatas = self._get_first_group(
            results=results,
            key=CHROMA_METADATAS_KEY,
        )

        distances = self._get_first_group(
            results=results,
            key=CHROMA_DISTANCES_KEY,
        )

        mapped_results: list[QuestionSearchResult] = []

        for index, question_id in enumerate(ids):
            metadata = self._get_metadata(
                metadatas=metadatas,
                index=index,
            )

            distance = self._get_distance(
                distances=distances,
                index=index,
            )

            question = self._question_mapper.to_question(
                metadata=metadata,
                fallback_question_id=str(question_id),
            )

            mapped_results.append(
                QuestionSearchResult(
                    question=question,
                    distance=distance,
                    score=DistanceScoreConverter.to_score(
                        distance=distance,
                    ),
                )
            )

        return mapped_results

    @staticmethod
    def _get_first_group(
        *,
        results: ChromaQueryResults,
        key: str,
    ) -> list[Any]:
        values = results.get(key)

        if not values or not isinstance(values, list):
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
    ) -> ChromaQuestionMetadata:
        metadata = cls._safe_get(
            values=metadatas,
            index=index,
            default={},
        )

        if not isinstance(metadata, dict):
            return {}

        return metadata

    @classmethod
    def _get_distance(
        cls,
        *,
        distances: list[Any],
        index: int,
    ) -> float:
        distance = cls._safe_get(
            values=distances,
            index=index,
            default=DEFAULT_RETRIEVAL_DISTANCE,
        )

        try:
            return float(distance)

        except (TypeError, ValueError) as exc:
            raise VectorStoreError(
                "Invalid Chroma distance value."
            ) from exc

    @staticmethod
    def _safe_get(
        *,
        values: list[Any],
        index: int,
        default: Any,
    ) -> Any:
        if index < 0 or index >= len(values):
            return default

        return values[index]