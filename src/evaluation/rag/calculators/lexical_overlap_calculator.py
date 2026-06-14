from __future__ import annotations


class LexicalOverlapCalculator:
    """
    Calculates lexical overlap score.
    """

    @staticmethod
    def calculate(
        *,
        answer_tokens: set[str],
        context_tokens: set[str],
    ) -> float:
        if not answer_tokens:
            return 0.0

        if not context_tokens:
            return 0.0

        supported_tokens = (
            answer_tokens
            & context_tokens
        )

        return (
            len(supported_tokens)
            / len(answer_tokens)
        )