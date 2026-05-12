from __future__ import annotations

from typing import Any

from src.domain.metadata.evaluation_metadata import (
    EvaluationMetadata,
)
from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)


NUMBER_TYPES = (int, float)


EVALUATION_RESULT_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "score": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_EVALUATION_SCORE,
        "max_value": MAX_EVALUATION_SCORE,
    },
    "feedback": {
        "type": str,
        "non_empty": True,
        "strip": True,
    },
    "technical_accuracy": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_EVALUATION_SCORE,
        "max_value": MAX_EVALUATION_SCORE,
    },
    "depth": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_EVALUATION_SCORE,
        "max_value": MAX_EVALUATION_SCORE,
    },
    "communication": {
        "type": NUMBER_TYPES,
        "finite": True,
        "min_value": MIN_EVALUATION_SCORE,
        "max_value": MAX_EVALUATION_SCORE,
    },
    "metadata": {
        "type": EvaluationMetadata,
    },
}