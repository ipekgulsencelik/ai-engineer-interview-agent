from __future__ import annotations

from typing import Protocol

from src.domain.entities.question import Question


class EvaluationPromptBuilder(Protocol):
    """
    Evaluation prompt generation contract.

    Bu interface:
        - evaluator prompt generation abstraction sağlar
        - provider-specific prompt formatını soyutlar
        - evaluator orchestration layer'ını concrete prompting implementation'dan ayırır

    Concrete implementasyon örnekleri:
        - RubricEvaluationPromptBuilder
        - StructuredJsonPromptBuilder
        - FewShotEvaluationPromptBuilder
        - ChainOfThoughtEvaluationPromptBuilder

    Bu interface:
        - LLM çağrısı yapmaz
        - parsing yapmaz
        - evaluation sonucu üretmez
        - business logic içermez
    """

    def build(
        self,
        *,
        question: Question,
        answer: str,
    ) -> str:
        """
        Evaluation için prompt üretir.

        Args:
            question:
                Değerlendirilecek Question domain entity'si.

            answer:
                Candidate tarafından verilen raw answer text.

        Returns:
            LLM'e gönderilecek normalize edilmiş prompt string'i.
        """
        ...