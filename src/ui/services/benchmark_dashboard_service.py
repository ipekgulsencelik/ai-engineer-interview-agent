from __future__ import annotations

from pathlib import Path

from src.infrastructure.loaders.benchmark_dataset_loader import (
    BenchmarkDatasetLoader,
)
from src.application.services.retrieval_benchmark_service import (
    RetrievalBenchmarkService,
)
from src.application.services.semantic_question_retrieval_service import (
    SemanticQuestionRetrievalService,
)
from src.infrastructure.embeddings.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)
from src.infrastructure.vector_store.chroma_question_vector_store import (
    ChromaQuestionVectorStore,
)
from src.ui.models.benchmark_dashboard_result import (
    BenchmarkDashboardResult,
)


class BenchmarkDashboardService:
    """
    Benchmark dashboard orchestration service.
    """

    @staticmethod
    def run() -> BenchmarkDashboardResult:
        dataset = BenchmarkDatasetLoader().load(
            Path(
                "data/benchmark/retrieval_benchmark.json",
            ),
        )

        retrieval_service = SemanticQuestionRetrievalService(
            embedding_provider=SentenceTransformerEmbeddingModel(),
            vector_store=ChromaQuestionVectorStore(),
        )

        benchmark_service = RetrievalBenchmarkService(
            retrieval_service=retrieval_service,
        )

        results = benchmark_service.run(
            dataset=dataset,
            top_k=5,
        )

        summary = benchmark_service.summarize(
            results=results,
        )

        return BenchmarkDashboardResult(
            summary=summary,
            results=results,
        )