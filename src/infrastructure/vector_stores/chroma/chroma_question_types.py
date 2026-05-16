from __future__ import annotations

from typing import NotRequired, TypedDict


class QuestionMetadata(TypedDict):
    id: str
    text: str
    category: str
    level: str
    difficulty: str
    question_type: str
    metadata_version: NotRequired[str]
    expected_points: NotRequired[list[str]]
    keywords: NotRequired[list[str]]
    market_weight: NotRequired[float | int | str]
    followup_allowed: NotRequired[bool | str]


class ChromaQueryPayload(TypedDict):
    query_embeddings: list[list[float]]
    n_results: int
    where: dict[str, str]


class ChromaQueryResults(TypedDict, total=False):
    metadatas: list[list[QuestionMetadata]]