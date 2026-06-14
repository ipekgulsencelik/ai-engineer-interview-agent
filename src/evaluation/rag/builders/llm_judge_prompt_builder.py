from __future__ import annotations

from src.evaluation.rag.value_objects.llm_judge_request import LLMJudgeRequest


class LLMJudgePromptBuilder:
    @staticmethod
    def build(*, request: LLMJudgeRequest) -> str:
        return (
            "Evaluate the RAG answer.\n"
            f"Question: {request.question}\n"
            f"Answer: {request.generated_answer}\n"
            f"Retrieved context: {request.retrieved_context}\n"
            f"Criteria: {request.evaluation_criteria}"
        )
