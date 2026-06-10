from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    RATIO_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EVALUATOR_ALIGNMENT_REPORT_SCHEMA: Final[SchemaDefinition] = {
    "report_id": NON_EMPTY_STRING_RULE,
    "evaluator_id": NON_EMPTY_STRING_RULE,
    "model_name": NON_EMPTY_STRING_RULE,
    "overall_alignment_score": RATIO_RULE,
    "interpretation": NON_EMPTY_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}