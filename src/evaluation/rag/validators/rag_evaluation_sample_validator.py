from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.rag_evaluation_sample_schema import (
    RAG_EVALUATION_SAMPLE_SCHEMA,
)


class RAGEvaluationSampleValidator:
    """
    RAGEvaluationSample validation service.
    """

    @staticmethod
    def validate(
        *,
        sample_id: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        question: str,
        expected_answer: str | None,
        expected_context: str | None,
        expected_chunk_ids: tuple[
            str,
            ...,
        ],
        metadata: dict[
            str,
            str,
        ] | None,
        tags: tuple[
            str,
            ...,
        ],
        difficulty: str | None,
        category: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_id": sample_id,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "question": question,
                "expected_answer": expected_answer,
                "expected_context": expected_context,
                "expected_chunk_ids": expected_chunk_ids,
                "metadata": (
                    metadata
                    or {}
                ),
                "tags": tags,
                "difficulty": difficulty,
                "category": category,
                "notes": notes,
            },
            schema=RAG_EVALUATION_SAMPLE_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        for index, chunk_id in enumerate(
            expected_chunk_ids,
        ):
            if not isinstance(
                chunk_id,
                str,
            ) or not chunk_id.strip():
                raise EvaluationValidationError(
                    f"expected_chunk_ids[{index}] must be non-empty string."
                )

        for index, tag in enumerate(
            tags,
        ):
            if not isinstance(
                tag,
                str,
            ) or not tag.strip():
                raise EvaluationValidationError(
                    f"tags[{index}] must be non-empty string."
                )

        if metadata is not None:
            for key, value in metadata.items():
                if not isinstance(
                    key,
                    str,
                ) or not key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )