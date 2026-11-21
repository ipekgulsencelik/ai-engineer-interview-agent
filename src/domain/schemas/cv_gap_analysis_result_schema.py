"""Validation schema for CV skill gap result values."""

from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import RATIO_RULE, STRING_TUPLE_RULE
from src.domain.validation.schema_types import ValidationSchema

CV_GAP_ANALYSIS_RESULT_SCHEMA: Final[ValidationSchema] = {
    "matched_skills": STRING_TUPLE_RULE,
    "missing_skills": STRING_TUPLE_RULE,
    "recommended_focus_areas": STRING_TUPLE_RULE,
    "alignment_score": RATIO_RULE,
}
