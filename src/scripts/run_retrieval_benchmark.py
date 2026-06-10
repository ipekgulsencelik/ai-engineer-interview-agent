from __future__ import annotations

from pathlib import Path

from src.application.benchmarking.loaders.benchmark_dataset_loader import (
    BenchmarkDatasetLoader,
)
from src.application.benchmarking.services.retrieval_benchmark_service import (
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


def main() -> None:
    dataset = BenchmarkDatasetLoader().load(
        Path("data/benchmark/retrieval_benchmark.json"),
    )

    retrieval_service = SemanticQuestionRetrievalService(
        embedding_model=SentenceTransformerEmbeddingModel(),
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

    print("\n=== RETRIEVAL BENCHMARK SUMMARY ===")
    print(f"total: {summary.total}")
    print(f"category_hit_rate: {summary.category_hit_rate}")
    print(
        "average_latency_seconds: "
        f"{summary.average_latency_seconds}"
    )
    print(f"average_top_score: {summary.average_top_score}")

    print("\n=== DETAILS ===")

    for result in results:
        print("-" * 60)
        print(f"Query: {result.query}")
        print(f"Expected Category: {result.expected_category}")
        print(f"Top Question ID: {result.top_question_id}")
        print(f"Top Score: {result.top_score}")
        print(f"Category Hit: {result.category_hit}")
        print(f"Latency: {result.latency_seconds:.4f}s")


if __name__ == "__main__":
    main()