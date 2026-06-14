from __future__ import annotations

from src.evaluation.rag.calculators.lexical_overlap_calculator import (
    LexicalOverlapCalculator,
)
from src.evaluation.rag.requests.faithfulness_evaluation_request import (
    FaithfulnessEvaluationRequest,
)
from src.evaluation.rag.tokenizers.text_tokenizer import (
    TextTokenizer,
)


class FaithfulnessEvaluator:
    """
    Faithfulness evaluation service.
    """

    def __init__(
        self,
        *,
        tokenizer: (
            TextTokenizer | None
        ) = None,
        overlap_calculator: (
            LexicalOverlapCalculator
            | None
        ) = None,
    ) -> None:
        self._tokenizer = (
            tokenizer
            or TextTokenizer()
        )

        self._overlap_calculator = (
            overlap_calculator
            or LexicalOverlapCalculator()
        )

    def evaluate(
        self,
        *,
        request: (
            FaithfulnessEvaluationRequest
        ),
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
            self._overlap_calculator.calculate(
                answer_tokens=answer_tokens,
                context_tokens=context_tokens,
            )
        )