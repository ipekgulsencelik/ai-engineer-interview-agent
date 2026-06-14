from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.rag_evaluation_sample_validator import (
    RAGEvaluationSampleValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGEvaluationSample:
    """
    Immutable RAG evaluation sample.

    Represents a single benchmark sample used to
    evaluate retrieval, grounding, faithfulness,
    answer relevancy, correctness, and hallucination
    behavior.
    """

    sample_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    question: str

    expected_answer: str | None = None

    expected_context: str | None = None

    expected_chunk_ids: tuple[
        str,
        ...,
    ] = ()

    metadata: dict[
        str,
        str,
    ] | None = None

    tags: tuple[
        str,
        ...,
    ] = ()

    difficulty: str | None = None

    category: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        RAGEvaluationSampleValidator.validate(
            sample_id=self.sample_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            question=self.question,
            expected_answer=self.expected_answer,
            expected_context=self.expected_context,
            expected_chunk_ids=self.expected_chunk_ids,
            metadata=self.metadata,
            tags=self.tags,
            difficulty=self.difficulty,
            category=self.category,
            notes=self.notes,
        )

    @property
    def has_expected_answer(
        self,
    ) -> bool:
        return self.expected_answer is not None

    @property
    def has_expected_context(
        self,
    ) -> bool:
        return self.expected_context is not None

    @property
    def has_expected_chunks(
        self,
    ) -> bool:
        return bool(
            self.expected_chunk_ids,
        )