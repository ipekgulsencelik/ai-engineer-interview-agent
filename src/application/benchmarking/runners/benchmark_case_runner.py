from __future__ import annotations

from src.application.builders.benchmark_scoring_context_builder import (
    BenchmarkScoringContextBuilder,
)
from src.application.factories.benchmark_result_factory import (
    BenchmarkResultFactory,
)
from src.infrastructure.models.benchmark_case import (
    BenchmarkCase,
)
from src.infrastructure.models.benchmark_result import (
    BenchmarkResult,
)
from src.application.policies.category_hit_policy import (
    CategoryHitPolicy,
)
from src.application.timing.execution_timer import (
    ExecutionTimer,
)
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)
from src.domain.retrieval.question_search_result import (
    QuestionSearchResult,
)


class BenchmarkCaseRunner:
    """
    Single benchmark case execution runner.
    """

    def __init__(
        self,
        *,
        retrieval_service: SemanticQuestionRetrievalService,
    ) -> None:
        self._retrieval_service = retrieval_service

    def run(
        self,
        *,
        benchmark_case: BenchmarkCase,
        top_k: int,
    ) -> BenchmarkResult:
        started_at = ExecutionTimer.current_timestamp()

        search_results = self._retrieve_results(
            benchmark_case=benchmark_case,
            top_k=top_k,
        )

        latency_seconds = ExecutionTimer.elapsed_since(
            started_at=started_at,
        )

        top_result = self._get_top_result(
            search_results=search_results,
        )

        return BenchmarkResultFactory.create(
            benchmark_case=benchmark_case,
            retrieved_count=len(search_results),
            top_question_id=(
                top_result.question.id
                if top_result is not None
                else None
            ),
            top_score=(
                top_result.score
                if top_result is not None
                else None
            ),
            category_hit=CategoryHitPolicy.has_hit(
                expected_category=benchmark_case.expected_category,
                search_results=search_results,
            ),
            latency_seconds=latency_seconds,
        )

    def _retrieve_results(
        self,
        *,
        benchmark_case: BenchmarkCase,
        top_k: int,
    ) -> list[QuestionSearchResult]:
        return self._retrieval_service.retrieve(
            query=benchmark_case.query,
            context=BenchmarkScoringContextBuilder.build(),
            top_k=top_k,
        )

    @staticmethod
    def _get_top_result(
        *,
        search_results: list[QuestionSearchResult],
    ) -> QuestionSearchResult | None:
        return (
            search_results[0]
            if search_results
            else None
        )