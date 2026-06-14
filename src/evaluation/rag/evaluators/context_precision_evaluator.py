from __future__ import annotations

from src.evaluation.rag.calculators.context_precision_score_calculator import (
    ContextPrecisionScoreCalculator,
)
from src.evaluation.rag.requests.context_precision_request import (
    ContextPrecisionRequest,
)
from src.evaluation.rag.tokenizers.text_tokenizer import (
    TextTokenizer,
)


class ContextPrecisionEvaluator:
    """
    Context precision evaluation service.
    """

    def __init__(
        self,
        *,
        tokenizer: (
            TextTokenizer | None
        ) = None,
        score_calculator: (
            ContextPrecisionScoreCalculator
            | None
        ) = None,
    ) -> None:
        self._tokenizer = (
            tokenizer
            or TextTokenizer()
        )

        self._score_calculator = (
            score_calculator
            or ContextPrecisionScoreCalculator()
        )

    def evaluate(
        self,
        *,
        request: ContextPrecisionRequest,
    ) -> float:
        answer_tokens = (
            self._tokenizer.tokenize(
                request.generated_answer,
            )
        )

        context_tokens = (
            self._tokenizer.tokenize(
                request.retrieved_context,
            )
        )

        return (
            self._score_calculator.calculate(
                answer_tokens=answer_tokens,
                context_tokens=context_tokens,
            )
        )