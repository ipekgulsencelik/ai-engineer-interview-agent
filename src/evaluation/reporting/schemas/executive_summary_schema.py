from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_RATIO_RULE,
    OPTIONAL_STRING_RULE,
    OPTIONAL_NUMBER_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXECUTIVE_SUMMARY_SCHEMA: Final[
    SchemaDefinition
] = {
    "summary_id": NON_EMPTY_STRING_RULE,
    "title": NON_EMPTY_STRING_RULE,
    "overall_assessment": NON_EMPTY_STRING_RULE,
    "key_findings": TUPLE_RULE,
    "strengths": TUPLE_RULE,
    "weaknesses": TUPLE_RULE,
    "recommendations": TUPLE_RULE,
    "overall_score": OPTIONAL_NUMBER_RULE,
    "pass_rate": OPTIONAL_RATIO_RULE,
    "total_runs": OPTIONAL_NUMBER_RULE,
    "average_score": OPTIONAL_NUMBER_RULE,
    "best_score": OPTIONAL_NUMBER_RULE,
    "risk_level": OPTIONAL_STRING_RULE,
    "trend_direction": OPTIONAL_STRING_RULE,
    "confidence_level": OPTIONAL_RATIO_RULE,
    "recommendation": OPTIONAL_STRING_RULE,
    "generated_by": OPTIONAL_STRING_RULE,
    "notes": OPTIONAL_STRING_RULE,
}