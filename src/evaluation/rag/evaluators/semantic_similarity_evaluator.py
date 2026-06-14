from __future__ import annotations

from src.evaluation.rag.calculators.semantic_similarity_score_calculator import (
    SemanticSimilarityScoreCalculator,
)
from src.evaluation.rag.requests.semantic_similarity_request import (
    SemanticSimilarityRequest,
)
from src.evaluation.rag.tokenizers.text_tokenizer import (
    TextTokenizer,
)


class SemanticSimilarityEvaluator:
    """
    Semantic similarity evaluation service.
    """

    def __init__(
        self,
        *,
        tokenizer: (
            TextTokenizer | None
        ) = None,
        score_calculator: (
            SemanticSimilarityScoreCalculator
            | None
        ) = None,
    ) -> None:
        self._tokenizer = (
            tokenizer
            or TextTokenizer()
        )

        self._score_calculator = (
            score_calculator
            or SemanticSimilarityScoreCalculator()
        )

    def evaluate(
        self,
        *,
        request: SemanticSimilarityRequest,
    ) -> float:
        reference_tokens = (
            self._tokenizer.tokenize(
                request.reference_text,
            )
        )

        candidate_tokens = (
            self._tokenizer.tokenize(
                request.candidate_text,
            )
        )

        return self._score_calculator.calculate(
            reference_tokens=reference_tokens,
            candidate_tokens=candidate_tokens,
        )