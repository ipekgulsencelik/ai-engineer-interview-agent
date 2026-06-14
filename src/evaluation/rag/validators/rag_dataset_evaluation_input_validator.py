from __future__ import annotations

from src.evaluation.rag.entities.rag_evaluation_sample import (
    RAGEvaluationSample,
)


class RAGDatasetEvaluationInputValidator:
    """
    Validates dataset-level RAG evaluation inputs.
    """

    @staticmethod
    def validate(
        *,
        samples: tuple[
            RAGEvaluationSample,
            ...,
        ],
        generated_answers: dict[
            str,
            str,
        ],
        retrieved_contexts: dict[
            str,
            str,
        ],
    ) -> None:
        if not samples:
            raise ValueError(
                "samples must not be empty."
            )

        missing_generated_answers = tuple(
            sample.sample_id
            for sample in samples
            if sample.sample_id not in generated_answers
        )

        if missing_generated_answers:
            raise ValueError(
                "generated_answers missing sample ids: "
                f"{missing_generated_answers}"
            )

        missing_retrieved_contexts = tuple(
            sample.sample_id
            for sample in samples
            if sample.sample_id not in retrieved_contexts
        )

        if missing_retrieved_contexts:
            raise ValueError(
                "retrieved_contexts missing sample ids: "
                f"{missing_retrieved_contexts}"
            )