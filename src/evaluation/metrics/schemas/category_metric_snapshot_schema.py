from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


CATEGORY_METRIC_SNAPSHOT_SCHEMA: Final[SchemaDefinition] = {
    "category": NON_EMPTY_STRING_RULE,
    "average_human_score": NON_NEGATIVE_NUMBER_RULE,
    "average_llm_score": NON_NEGATIVE_NUMBER_RULE,
    "overall_alignment_score": RATIO_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}