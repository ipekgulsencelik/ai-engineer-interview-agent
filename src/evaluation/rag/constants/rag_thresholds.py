from __future__ import annotations

from typing import Final


MINIMUM_RETRIEVAL_PRECISION: Final[
    float
] = 0.70

MINIMUM_RETRIEVAL_RECALL: Final[
    float
] = 0.70

MINIMUM_CONTEXT_RELEVANCE_SCORE: Final[
    float
] = 0.75

MINIMUM_FAITHFULNESS_SCORE: Final[
    float
] = 0.80

MINIMUM_ANSWER_RELEVANCE_SCORE: Final[
    float
] = 0.75

MINIMUM_ANSWER_CORRECTNESS_SCORE: Final[
    float
] = 0.75

MINIMUM_OVERALL_RAG_SCORE: Final[
    float
] = 0.80

MAXIMUM_ACCEPTABLE_HALLUCINATION_RATE: Final[
    float
] = 0.0