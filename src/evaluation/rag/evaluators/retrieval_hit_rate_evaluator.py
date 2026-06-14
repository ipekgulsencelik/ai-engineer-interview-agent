from __future__ import annotations

from src.evaluation.rag.value_objects.retrieval_hit_rate_request import (
    RetrievalHitRateRequest,
)


class RetrievalHitRateEvaluator:
    """
    Evaluates retrieval hit-rate.

    Returns 1.0 when the expected chunk appears
    in the retrieved chunk ids, otherwise 0.0.
    """

    def evaluate(
        self,
        *,
        request: RetrievalHitRateRequest,
    ) -> float:
        retrieved_top_k = (
            request.retrieved_chunk_ids[
                : request.top_k
            ]
        )

        if (
            request.expected_chunk_id
            in retrieved_top_k
        ):
            return 1.0

        return 0.0