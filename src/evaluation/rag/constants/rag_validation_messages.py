from __future__ import annotations

from typing import Final


RESULTS_MUST_BE_TUPLE: Final[str] = (
    "results must be tuple."
)

INVALID_RESULT_ITEM: Final[str] = (
    "results[{index}] must be RAGEvaluationResult."
)

SAMPLE_COUNT_MISMATCH: Final[str] = (
    "sample_count must equal len(results)."
)

PASS_FAIL_COUNT_MISMATCH: Final[str] = (
    "passed_count + failed_count must equal sample_count."
)

HALLUCINATION_COUNT_EXCEEDED: Final[str] = (
    "hallucination_count cannot exceed sample_count."
)

PASS_RATE_MISMATCH: Final[str] = (
    "pass_rate mismatch."
)

HALLUCINATION_RATE_MISMATCH: Final[str] = (
    "hallucination_rate mismatch."
)