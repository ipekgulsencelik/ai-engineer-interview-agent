from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.llm_judge_request_validator import (
    LLMJudgeRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class LLMJudgeRequest:
    """
    Request model for LLM-as-a-judge evaluation.

    Represents the inputs required to evaluate
    a generated answer using an LLM judge.
    """

    question: str

    generated_answer: str

    retrieved_context: str

    evaluation_criteria: str

    model_name: str | None = None

    judge_model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        LLMJudgeRequestValidator.validate(
            question=self.question,
            generated_answer=self.generated_answer,
            retrieved_context=self.retrieved_context,
            evaluation_criteria=self.evaluation_criteria,
            model_name=self.model_name,
            judge_model_name=self.judge_model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )