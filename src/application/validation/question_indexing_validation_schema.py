from __future__ import annotations

from typing import Any

from src.domain.entities.question import Question


QUESTION_INDEXING_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "questions": {
        "collection_type": list,
        "item_type": Question,
        "non_empty": True,
    },
}