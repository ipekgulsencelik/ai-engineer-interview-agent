from __future__ import annotations

from typing import NotRequired
from typing import TypeAlias
from typing import TypedDict


class ChromaQuestionMetadata(
    TypedDict,
    total=False,
):
    question_id: str
    text: str
    category: str
    level: str
    difficulty: int
    question_type: str

    expected_points: NotRequired[
        list[str]
    ]

    keywords: NotRequired[
        list[str]
    ]

    market_weight: NotRequired[
        float
    ]

    followup_allowed: NotRequired[
        bool
    ]

    followup: NotRequired[
        str | None
    ]

    ideal_answer_hint: NotRequired[
        str | None
    ]


ChromaDifficultyFilter: TypeAlias = dict[
    str,
    int,
]


ChromaWhereFilterValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | ChromaDifficultyFilter
)


ChromaWhereFilter: TypeAlias = dict[
    str,
    ChromaWhereFilterValue,
]


class ChromaQueryPayload(
    TypedDict,
    total=False,
):
    query_embeddings: list[list[float]]

    n_results: int

    where: ChromaWhereFilter


class ChromaQueryResults(
    TypedDict,
    total=False,
):
    ids: list[list[str]]

    documents: list[list[str]]

    metadatas: list[
        list[ChromaQuestionMetadata]
    ]

    distances: list[list[float]]


QuestionVectorMetadata: TypeAlias = dict[
    str,
    str
    | int
    | float
    | bool
    | list[str]
    | None,
]