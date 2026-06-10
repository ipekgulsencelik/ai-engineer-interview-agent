from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.domain.enums.level import Level
from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.domain.schemas.evaluation_sample_schema import (
    EVALUATION_SAMPLE_SCHEMA,
)


class EvaluationSampleValidator:
    """
    EvaluationSample entity validation service.
    """

    @classmethod
    def validate(
        cls,
        *,
        sample_id: str,
        question_id: str,
        question: str,
        candidate_answer: str,
        expected_answer: str,
        category: str,
        level: Level,
        retrieved_contexts: tuple[str, ...],
        metadata: Mapping[str, Any],
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_id": sample_id,
                "question_id": question_id,
                "question": question,
                "candidate_answer": candidate_answer,
                "expected_answer": expected_answer,
                "category": category,
                "retrieved_contexts": retrieved_contexts,
                "metadata": metadata,
            },
            schema=EVALUATION_SAMPLE_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        cls._validate_level(level)

    @staticmethod
    def _validate_level(level: Level) -> None:
        if not isinstance(level, Level):
            raise EvaluationValidationError(
                "level must be a Level enum."
            )