from __future__ import annotations

from src.domain.constants.chroma_question import (
    REQUIRED_QUESTION_METADATA_FIELDS,
)

CHROMA_QUESTION_METADATA_SCHEMA = {
    field: {"required": True, "type": (int, str)}
    if field == "difficulty"
    else {"required": True, "type": str}
    for field in REQUIRED_QUESTION_METADATA_FIELDS
}

CHROMA_QUESTION_METADATA_SCHEMA.update(
    {
        "metadata_version": {"required": False, "type": str},
        "expected_points": {"required": False, "type": list},
        "keywords": {"required": False, "type": list},
        "market_weight": {"required": False, "type": (int, float, str)},
        "followup_allowed": {"required": False, "type": (bool, str)},
    }
)