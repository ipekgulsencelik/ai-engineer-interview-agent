from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.llm_judge_request_schema import (
    LLM_JUDGE_REQUEST_SCHEMA,
)


class LLMJudgeRequestValidator:
    """
    LLMJudgeRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        generated_answer: str,
        retrieved_context: str,
        evaluation_criteria: str,
        model_name: str | None,
        judge_model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "generated_answer": generated_answer,
                "retrieved_context": retrieved_context,
                "evaluation_criteria": evaluation_criteria,
                "model_name": model_name,
                "judge_model_name": judge_model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=LLM_JUDGE_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )