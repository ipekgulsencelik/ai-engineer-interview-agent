from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


RAG_EVALUATION_RESULT_SCHEMA: Final[
    SchemaDefinition
] = {
    "result_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "sample_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "retriever_name": NON_EMPTY_STRING_RULE,
    "evaluator_name": NON_EMPTY_STRING_RULE,
    "query": NON_EMPTY_STRING_RULE,
    "generated_answer": NON_EMPTY_STRING_RULE,
    "expected_answer": OPTIONAL_STRING_RULE,
    "retrieved_context_count": NON_NEGATIVE_NUMBER_RULE,
    "relevant_context_count": NON_NEGATIVE_NUMBER_RULE,
    "retrieval_precision": RATIO_RULE,
    "retrieval_recall": RATIO_RULE,
    "context_relevance_score": RATIO_RULE,
    "faithfulness_score": RATIO_RULE,
    "answer_relevance_score": RATIO_RULE,
    "answer_correctness_score": RATIO_RULE,
    "overall_score": RATIO_RULE,
    "hallucination_detected": BOOLEAN_RULE,
    "passed": BOOLEAN_RULE,
    "latency_ms": NON_NEGATIVE_NUMBER_RULE,
    "created_at": DATETIME_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}