from __future__ import annotations

from typing import Final


RAG_EVALUATION_PASSED: Final[
    str
] = (
    "rag_evaluation_passed"
)

RAG_FAILED_DUE_TO_HALLUCINATION: Final[
    str
] = (
    "rag_failed_due_to_hallucination"
)

RAG_FAILED_DUE_TO_LOW_RETRIEVAL_PRECISION: Final[
    str
] = (
    "rag_failed_due_to_low_retrieval_precision"
)

RAG_FAILED_DUE_TO_LOW_RETRIEVAL_RECALL: Final[
    str
] = (
    "rag_failed_due_to_low_retrieval_recall"
)

RAG_FAILED_DUE_TO_LOW_CONTEXT_RELEVANCE: Final[
    str
] = (
    "rag_failed_due_to_low_context_relevance"
)

RAG_FAILED_DUE_TO_LOW_FAITHFULNESS: Final[
    str
] = (
    "rag_failed_due_to_low_faithfulness"
)

RAG_FAILED_DUE_TO_LOW_ANSWER_RELEVANCE: Final[
    str
] = (
    "rag_failed_due_to_low_answer_relevance"
)

RAG_FAILED_DUE_TO_LOW_ANSWER_CORRECTNESS: Final[
    str
] = (
    "rag_failed_due_to_low_answer_correctness"
)

RAG_FAILED_DUE_TO_LOW_OVERALL_SCORE: Final[
    str
] = (
    "rag_failed_due_to_low_overall_score"
)