from __future__ import annotations

from typing import Final


HUMAN_ANNOTATION_REQUIRED_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "sample_id",
        "evaluator_id",
        "overall_score",
        "technical_score",
        "communication_score",
        "feedback",
    }
)