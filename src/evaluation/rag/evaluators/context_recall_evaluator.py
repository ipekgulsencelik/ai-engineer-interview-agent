from __future__ import annotations

from src.evaluation.rag.calculators.context_recall_score_calculator import (
    ContextRecallScoreCalculator,
)
from src.evaluation.rag.requests.context_recall_request import (
    ContextRecallRequest,
)
from src.evaluation.rag.tokenizers.text_tokenizer import (
    TextTokenizer,
)


class ContextRecallEvaluator:
    """
    Context recall evaluation service.
    """

    def __init__(
        self,
        *,
        tokenizer: (
            TextTokenizer | None
        ) = None,
        score_calculator: (
            ContextRecallScoreCalculator
            | None
        ) = None,
    ) -> None:
        self._tokenizer = (
            tokenizer
            or TextTokenizer()
        )

        self._score_calculator = (
            score_calculator
            or ContextRecallScoreCalculator()
        )

    def evaluate(
        self,
        *,
        request: ContextRecallRequest,
    ) -> float:
        expected_context_tokens = (
            self._tokenizer.tokenize(
                request.expected_context,
            )
        )

        retrieved_context_tokens = (
            self._tokenizer.tokenize(
                request.retrieved_context,
            )
        )

        return (
            self._score_calculator.calculate(
                expected_context_tokens=(
                    expected_context_tokens
                ),
                retrieved_context_tokens=(
                    retrieved_context_tokens
                ),
            )
        )