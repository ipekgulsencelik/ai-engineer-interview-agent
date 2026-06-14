from __future__ import annotations

from datetime import datetime

from typing import Final

from src.domain.validation.common_rules import (
    DATETIME_RULE,
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)
from src.domain.validation.schema_rules import ValidationRule

DATETIME_OBJECT_RULE = ValidationRule(expected_type=datetime)


RAG_EVALUATION_REPORT_SCHEMA: Final[
    SchemaDefinition
] = {
    "report_id": NON_EMPTY_STRING_RULE,
    "experiment_id": NON_EMPTY_STRING_RULE,
    "benchmark_id": NON_EMPTY_STRING_RULE,
    "benchmark_name": NON_EMPTY_STRING_RULE,
    "benchmark_version": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "retriever_name": NON_EMPTY_STRING_RULE,
    "evaluator_name": NON_EMPTY_STRING_RULE,
    "results": TUPLE_RULE,
    "sample_count": NON_NEGATIVE_NUMBER_RULE,
    "average_retrieval_precision": RATIO_RULE,
    "average_retrieval_recall": RATIO_RULE,
    "average_context_relevance_score": RATIO_RULE,
    "average_faithfulness_score": RATIO_RULE,
    "average_answer_relevance_score": RATIO_RULE,
    "average_answer_correctness_score": RATIO_RULE,
    "average_overall_score": RATIO_RULE,
    "hallucination_count": NON_NEGATIVE_NUMBER_RULE,
    "hallucination_rate": RATIO_RULE,
    "passed_count": NON_NEGATIVE_NUMBER_RULE,
    "failed_count": NON_NEGATIVE_NUMBER_RULE,
    "pass_rate": RATIO_RULE,
    "generated_at": DATETIME_OBJECT_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}