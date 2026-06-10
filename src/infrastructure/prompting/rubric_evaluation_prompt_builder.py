from __future__ import annotations

from src.application.ports.evaluation_prompt_builder import (
    EvaluationPromptBuilder,
)
from src.domain.entities.question import Question


class RubricEvaluationPromptBuilder(
    EvaluationPromptBuilder,
):
    """
    Rubric-driven evaluation prompt builder implementasyonudur.

    Bu sınıf:
        - Question ve candidate answer üzerinden
          evaluation prompt üretir
        - provider-independent prompting abstraction sağlar

    Bu sınıf:
        - LLM çağrısı yapmaz
        - parsing yapmaz
        - evaluation sonucu üretmez
    """

    def build(
        self,
        *,
        question: Question,
        answer: str,
    ) -> str:
        expected_points = self._format_expected_points(
            question.expected_points,
        )

        keywords = self._format_keywords(
            question.keywords,
        )

        return f"""
        You are a senior AI engineering interviewer.

        Evaluate the candidate answer using the rubric below.

        QUESTION:
        {question.text}

        CATEGORY:
        {self._enum_value(question.category)}

        LEVEL:
        {self._enum_value(question.level)}

        QUESTION TYPE:
        {self._enum_value(question.question_type)}

        EXPECTED POINTS:
        {expected_points}

        EXPECTED KEYWORDS:
        {keywords}

        CANDIDATE ANSWER:
        {answer}

        Return ONLY valid JSON.

        JSON schema:

        {{
            "score": float,
            "feedback": str,
            "technical_accuracy": float,
            "depth": float,
            "communication": float,
            "missing_keywords": list[str],
            "follow_up_question": str,
            "confidence": float,
            "rubric_version": str
        }}
        """.strip()

    @staticmethod
    def _format_expected_points(
        expected_points: tuple[str, ...],
    ) -> str:
        if not expected_points:
            return "None"

        return "\n".join(
            f"- {point}"
            for point in expected_points
        )

    @staticmethod
    def _format_keywords(
        keywords: tuple[str, ...],
    ) -> str:
        if not keywords:
            return "None"

        return ", ".join(keywords)

    @staticmethod
    def _enum_value(
        value: object,
    ) -> object:
        return getattr(value, "value", value)