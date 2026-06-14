from __future__ import annotations

from datetime import UTC, datetime

from src.evaluation.rag.entities.rag_evaluation_sample import RAGEvaluationSample
from src.evaluation.rag.value_objects.rag_evaluation_result import RAGEvaluationResult


def rag_sample(**overrides: object) -> RAGEvaluationSample:
    data = {
        "sample_id": "sample-1",
        "benchmark_id": "rag-benchmark",
        "benchmark_name": "RAG Benchmark",
        "benchmark_version": "1.0.0",
        "question": "What does RAG use to ground answers?",
        "expected_answer": "RAG grounds answers in retrieved context.",
        "expected_context": "Retrieved context grounds RAG answers.",
        "expected_chunk_ids": ("chunk-1",),
        "metadata": {"source": "unit-test"},
        "tags": ("rag", "retrieval"),
        "difficulty": "medium",
        "category": "retrieval",
        "notes": "fixture",
    }
    data.update(overrides)
    return RAGEvaluationSample(**data)  # type: ignore[arg-type]


def rag_result(**overrides: object) -> RAGEvaluationResult:
    data = {
        "result_id": "result-1",
        "experiment_id": "experiment-1",
        "benchmark_id": "rag-benchmark",
        "benchmark_name": "RAG Benchmark",
        "benchmark_version": "1.0.0",
        "sample_id": "sample-1",
        "model_name": "model-a",
        "retriever_name": "retriever-a",
        "evaluator_name": "evaluator-a",
        "query": "What does RAG use to ground answers?",
        "generated_answer": "RAG uses retrieved context.",
        "expected_answer": "RAG grounds answers in retrieved context.",
        "retrieved_context_count": 2,
        "relevant_context_count": 1,
        "retrieval_precision": 0.5,
        "retrieval_recall": 1.0,
        "context_relevance_score": 0.75,
        "faithfulness_score": 0.8,
        "answer_relevance_score": 0.85,
        "answer_correctness_score": 0.9,
        "overall_score": 0.8,
        "hallucination_detected": False,
        "passed": True,
        "latency_ms": 12.5,
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        "interpretation": "rag_evaluation_passed",
        "notes": "fixture",
    }
    data.update(overrides)
    return RAGEvaluationResult(**data)  # type: ignore[arg-type]

from src.evaluation.rag.entities.rag_evaluation_report import RAGEvaluationReport
from src.evaluation.rag.value_objects.conversation_turn import ConversationTurn
from src.evaluation.rag.value_objects.turn_rag_result import TurnRAGResult


def rag_report(**overrides: object) -> RAGEvaluationReport:
    result = rag_result()
    data = {
        "report_id": "report-1",
        "experiment_id": "experiment-1",
        "benchmark_id": "rag-benchmark",
        "benchmark_name": "RAG Benchmark",
        "benchmark_version": "1.0.0",
        "model_name": "model-a",
        "retriever_name": "retriever-a",
        "evaluator_name": "evaluator-a",
        "results": (result,),
        "sample_count": 1,
        "average_retrieval_precision": result.retrieval_precision,
        "average_retrieval_recall": result.retrieval_recall,
        "average_context_relevance_score": result.context_relevance_score,
        "average_faithfulness_score": result.faithfulness_score,
        "average_answer_relevance_score": result.answer_relevance_score,
        "average_answer_correctness_score": result.answer_correctness_score,
        "average_overall_score": result.overall_score,
        "hallucination_count": 0,
        "hallucination_rate": 0.0,
        "passed_count": 1,
        "failed_count": 0,
        "pass_rate": 1.0,
        "generated_at": datetime(2026, 1, 1, tzinfo=UTC),
        "interpretation": "rag_report_passed",
        "notes": "fixture",
    }
    data.update(overrides)
    return RAGEvaluationReport(**data)  # type: ignore[arg-type]


def conversation_turn(**overrides: object) -> ConversationTurn:
    data = {
        "turn_id": "turn-1",
        "conversation_id": "conversation-1",
        "turn_index": 0,
        "user_message": "What is RAG?",
        "assistant_message": "RAG uses retrieved context.",
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        "retrieved_context": "RAG uses retrieved context.",
        "model_name": "model-a",
        "retriever_name": "retriever-a",
        "notes": "fixture",
    }
    data.update(overrides)
    return ConversationTurn(**data)  # type: ignore[arg-type]


def turn_rag_result(**overrides: object) -> TurnRAGResult:
    data = {
        "turn_index": 0,
        "faithfulness_score": 1.0,
        "answer_relevancy_score": 0.5,
        "context_precision_score": 1.0,
        "overall_score": 0.8333333333333334,
    }
    data.update(overrides)
    return TurnRAGResult(**data)  # type: ignore[arg-type]

from src.evaluation.rag.entities.experiment_node import ExperimentNode


def experiment_node(**overrides: object) -> ExperimentNode:
    data = {
        "experiment_id": "experiment-root",
        "experiment_name": "RAG Experiment",
        "experiment_version": "1.0.0",
        "parent_experiment_id": None,
        "overall_score": 0.8,
        "pass_rate": 1.0,
        "sample_count": 1,
        "passed_count": 1,
        "failed_count": 0,
        "tags": ("rag",),
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
    }
    data.update(overrides)
    return ExperimentNode(**data)  # type: ignore[arg-type]
