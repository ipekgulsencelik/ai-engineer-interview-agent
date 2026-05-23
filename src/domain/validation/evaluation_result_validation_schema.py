from __future__ import annotations

from typing import Final

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.metadata.evaluation_metadata import (
    EvaluationMetadata,
)
from src.domain.validation.schema_types import (
    ValidationRule,
    ValidationSchema,
)


NUMBER_TYPES = (int, float)


EVALUATION_SCORE_RULE: Final[
    ValidationRule
] = {
    "type": NUMBER_TYPES,
    "nullable": False,
    "reject_bool": True,
    "finite": True,
    "min_value": MIN_EVALUATION_SCORE,
    "max_value": MAX_EVALUATION_SCORE,
}


FEEDBACK_RULE: Final[
    ValidationRule
] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
    "strip": True,
}


METADATA_RULE: Final[
    ValidationRule
] = {
    "type": EvaluationMetadata,
    "nullable": False,
}


EVALUATION_RESULT_VALIDATION_SCHEMA: Final[
    ValidationSchema
] = {
    "score": EVALUATION_SCORE_RULE,
    "feedback": FEEDBACK_RULE,
    "technical_accuracy": EVALUATION_SCORE_RULE,
    "depth": EVALUATION_SCORE_RULE,
    "communication": EVALUATION_SCORE_RULE,
    "metadata": METADATA_RULE,
}