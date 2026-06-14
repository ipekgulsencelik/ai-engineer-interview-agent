from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


RAG_METRICS_SNAPSHOT_SCHEMA: Final[
    SchemaDefinition
] = {
    "average_retrieval_precision": RATIO_RULE,
    "average_retrieval_recall": RATIO_RULE,
    "average_context_relevance_score": RATIO_RULE,
    "average_faithfulness_score": RATIO_RULE,
    "average_answer_relevance_score": RATIO_RULE,
    "average_answer_correctness_score": RATIO_RULE,
    "average_overall_score": RATIO_RULE,
}