from __future__ import annotations

from src.domain.entities.question import Question
from src.domain.evaluation.evaluator import (
    Evaluator,
)
from src.domain.results.evaluation_result import (
    EvaluationResult,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class AnswerEvaluationServiceValidator(
    BaseSchemaValidator,
):
    """
    AnswerEvaluationService input/output validation helper.
    """

    @classmethod
    def validate_evaluator(
        cls,
        *,
        evaluator: Evaluator,
    ) -> None:
        if not hasattr(evaluator, "evaluate"):
            raise TypeError(
                "evaluator must implement evaluate()."
            )

    @classmethod
    def validate_evaluation_input(
        cls,
        *,
        question: Question,
        answer: str,
    ) -> str:
        cls.validate_model_type(
            value=question,
            expected_type=Question,
            field_name="question",
        )

        if not isinstance(answer, str):
            raise TypeError(
                "answer must be a string."
            )

        normalized_answer = answer.strip()

        if not normalized_answer:
            raise ValueError(
                "answer cannot be empty."
            )

        return normalized_answer

    @classmethod
    def validate_result(
        cls,
        *,
        result: EvaluationResult,
    ) -> None:
        cls.validate_model_type(
            value=result,
            expected_type=EvaluationResult,
            field_name="result",
        )