from __future__ import annotations

from src.evaluation.rag.value_objects.rag_evaluation_result import (
    RAGEvaluationResult,
)


class RAGReportCountCalculator:
    """
    Calculates RAG report counts.
    """

    @staticmethod
    def sample_count(
        *,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
    ) -> int:
        return len(
            results,
        )

    @staticmethod
    def hallucination_count(
        *,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
    ) -> int:
        return sum(
            result.hallucination_detected
            for result in results
        )

    @staticmethod
    def passed_count(
        *,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
    ) -> int:
        return sum(
            result.passed
            for result in results
        )

    @staticmethod
    def failed_count(
        *,
        results: tuple[
            RAGEvaluationResult,
            ...,
        ],
    ) -> int:
        return sum(
            not result.passed
            for result in results
        )