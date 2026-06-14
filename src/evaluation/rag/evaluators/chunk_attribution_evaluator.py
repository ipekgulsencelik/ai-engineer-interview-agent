from __future__ import annotations

from src.evaluation.rag.calculators.chunk_attribution_score_calculator import (
    ChunkAttributionScoreCalculator,
)
from src.evaluation.rag.counters.matched_token_counter import (
    MatchedTokenCounter,
)
from src.evaluation.rag.factories.chunk_attribution_result_factory import (
    ChunkAttributionResultFactory,
)
from src.evaluation.rag.requests.chunk_attribution_request import (
    ChunkAttributionRequest,
)
from src.evaluation.rag.tokenizers.text_tokenizer import (
    TextTokenizer,
)
from src.evaluation.rag.value_objects.chunk_attribution_result import (
    ChunkAttributionResult,
)


class ChunkAttributionEvaluator:
    """
    Evaluates attribution of retrieved chunks.
    """

    def __init__(
        self,
        *,
        tokenizer: (
            TextTokenizer | None
        ) = None,
        matched_token_counter: (
            MatchedTokenCounter | None
        ) = None,
        score_calculator: (
            ChunkAttributionScoreCalculator
            | None
        ) = None,
        result_factory: (
            ChunkAttributionResultFactory
            | None
        ) = None,
    ) -> None:
        self._tokenizer = (
            tokenizer
            or TextTokenizer()
        )

        self._matched_token_counter = (
            matched_token_counter
            or MatchedTokenCounter()
        )

        self._score_calculator = (
            score_calculator
            or ChunkAttributionScoreCalculator()
        )

        self._result_factory = (
            result_factory
            or ChunkAttributionResultFactory()
        )

    def evaluate(
        self,
        *,
        request: ChunkAttributionRequest,
    ) -> tuple[
        ChunkAttributionResult,
        ...,
    ]:
        answer_tokens = (
            self._tokenizer.tokenize(
                request.generated_answer,
            )
        )

        results: list[
            ChunkAttributionResult
        ] = []

        for chunk in request.retrieved_chunks:
            chunk_tokens = (
                self._tokenizer.tokenize(
                    chunk.chunk_text,
                )
            )

            matched_tokens = (
                self._matched_token_counter.count(
                    answer_tokens=answer_tokens,
                    chunk_tokens=chunk_tokens,
                )
            )

            attribution_score = (
                self._score_calculator.calculate(
                    matched_tokens=matched_tokens,
                    answer_token_count=len(
                        answer_tokens,
                    ),
                )
            )

            results.append(
                self._result_factory.create(
                    chunk=chunk,
                    attribution_score=(
                        attribution_score
                    ),
                    chunk_token_count=len(
                        chunk_tokens,
                    ),
                    matched_tokens=matched_tokens,
                )
            )

        return tuple(
            results,
        )