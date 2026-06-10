from __future__ import annotations

from typing import Final

from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)
from src.domain.validation.validation_rules import (
    FINITE_NUMBER_RULE,
)


STRING_TUPLE_RULE: Final[ValidationRule] = {
    "type": tuple,
    "nullable": False,
    "item_type": str,
}


CV_GAP_ANALYSIS_RESULT_SCHEMA: Final[ValidationSchema] = {
    "matched_skills": STRING_TUPLE_RULE,
    "missing_skills": STRING_TUPLE_RULE,
    "recommended_focus_areas": STRING_TUPLE_RULE,
    "alignment_score": {
        **FINITE_NUMBER_RULE,
        "min_value": 0,
        "max_value": 1,
    },
}