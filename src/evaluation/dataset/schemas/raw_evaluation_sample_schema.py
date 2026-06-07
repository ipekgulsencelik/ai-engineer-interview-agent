from __future__ import annotations

from typing import Final


REQUIRED_EVALUATION_SAMPLE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "sample_id",
        "question_id",
        "question",
        "candidate_answer",
        "expected_answer",
        "category",
        "level",
    }
)