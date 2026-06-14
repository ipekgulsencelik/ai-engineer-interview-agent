from __future__ import annotations

from src.evaluation.rag.calculators.answer_relevancy_score_calculator import (
    AnswerRelevancyScoreCalculator,
)
from src.evaluation.rag.value_objects.answer_relevancy_request import (
    AnswerRelevancyRequest,
)
from src.evaluation.rag.tokenizers.text_tokenizer import (
    TextTokenizer,
)


class AnswerRelevancyEvaluator:
    """
    Answer relevancy evaluation service.
    """

    def __init__(
        self,
        *,
        tokenizer: (
            TextTokenizer | None
        ) = None,
        score_calculator: (
            AnswerRelevancyScoreCalculator
            | None
        ) = None,
    ) -> None:
        self._tokenizer = (
            tokenizer
            or TextTokenizer()
        )

        self._score_calculator = (
            score_calculator
            or AnswerRelevancyScoreCalculator()
        )

    def evaluate(
        self,
        *,
        request: AnswerRelevancyRequest,
    ) -> float:
        question_tokens = (
            self._tokenizer.tokenize(
                request.question,
            )
        )

        answer_tokens = (
            self._tokenizer.tokenize(
                request.generated_answer,
            )
        )

        return (
            self._score_calculator.calculate(
                question_tokens=question_tokens,
                answer_tokens=answer_tokens,
            )
        )