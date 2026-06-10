from __future__ import annotations

from src.infrastructure.models.benchmark_case import (
    BenchmarkCase,
)
from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)
from src.infrastructure.models.benchmark_summary import (
    BenchmarkSummary,
)
from src.application.benchmarking.runners.benchmark_case_runner import (
    BenchmarkCaseRunner,
)
from src.application.benchmarking.summarizers.benchmark_summary_calculator import (
    BenchmarkSummaryCalculator,
)
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)


class RetrievalBenchmarkService:
    """
    Semantic retrieval benchmark orchestration service.
    """

    def __init__(
        self,
        *,
        retrieval_service: SemanticQuestionRetrievalService,
    ) -> None:
        self._case_runner = BenchmarkCaseRunner(
            retrieval_service=retrieval_service,
        )

    def run(
        self,
        *,
        dataset: list[BenchmarkCase],
        top_k: int = 5,
    ) -> list[BenchmarkResult]:
        return [
            self._case_runner.run(
                benchmark_case=benchmark_case,
                top_k=top_k,
            )
            for benchmark_case in dataset
        ]

    @staticmethod
    def summarize(
        *,
        results: list[BenchmarkResult],
    ) -> BenchmarkSummary:
        return BenchmarkSummaryCalculator.calculate(
            results=results,
        )