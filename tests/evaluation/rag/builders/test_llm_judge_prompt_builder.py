from __future__ import annotations

from src.evaluation.rag.builders.llm_judge_prompt_builder import LLMJudgePromptBuilder
from src.evaluation.rag.value_objects.llm_judge_request import LLMJudgeRequest


def test_llm_judge_prompt_builder_should_include_question_answer_context_and_criteria() -> None:
    prompt = LLMJudgePromptBuilder.build(
        request=LLMJudgeRequest(
            question="What is RAG?",
            generated_answer="It retrieves context.",
            retrieved_context="RAG retrieves context before answering.",
            evaluation_criteria="Score groundedness.",
        )
    )

    assert "What is RAG?" in prompt
    assert "It retrieves context." in prompt
    assert "RAG retrieves context" in prompt
    assert "Score groundedness." in prompt
