"""RAG validators."""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "AnswerRelevancyRequestValidator": "src.evaluation.rag.validators.answer_relevancy_request_validator",
    "ChunkAttributionRequestValidator": "src.evaluation.rag.validators.chunk_attribution_request_validator",
    "ChunkAttributionResultValidator": "src.evaluation.rag.validators.chunk_attribution_result_validator",
    "ContextPrecisionRequestValidator": "src.evaluation.rag.validators.context_precision_request_validator",
    "ContextRecallRequestValidator": "src.evaluation.rag.validators.context_recall_request_validator",
    "ConversationTurnValidator": "src.evaluation.rag.validators.conversation_turn_validator",
    "ExperimentLineageGraphValidator": "src.evaluation.rag.validators.experiment_lineage_graph_validator",
    "ExperimentLineageValidator": "src.evaluation.rag.validators.experiment_lineage_validator",
    "ExperimentNodeValidator": "src.evaluation.rag.validators.experiment_node_validator",
    "FaithfulnessEvaluationRequestValidator": "src.evaluation.rag.validators.faithfulness_evaluation_request_validator",
    "HallucinationRequestValidator": "src.evaluation.rag.validators.hallucination_request_validator",
    "HallucinationResultValidator": "src.evaluation.rag.validators.hallucination_result_validator",
    "LLMJudgeRequestValidator": "src.evaluation.rag.validators.llm_judge_request_validator",
    "MultiTurnRAGRequestValidator": "src.evaluation.rag.validators.multi_turn_rag_request_validator",
    "MultiTurnRAGResultValidator": "src.evaluation.rag.validators.multi_turn_rag_result_validator",
    "RAGDatasetEvaluationInputValidator": "src.evaluation.rag.validators.rag_dataset_evaluation_input_validator",
    "RAGDatasetRunResultValidator": "src.evaluation.rag.validators.rag_dataset_run_result_validator",
    "RAGEvaluationReportValidator": "src.evaluation.rag.validators.rag_evaluation_report_validator",
    "RAGEvaluationResultValidator": "src.evaluation.rag.validators.rag_evaluation_result_validator",
    "RAGEvaluationSampleValidator": "src.evaluation.rag.validators.rag_evaluation_sample_validator",
    "RAGMetricsSnapshotValidator": "src.evaluation.rag.validators.rag_metrics_snapshot_validator",
    "RetrievalHitRateRequestValidator": "src.evaluation.rag.validators.retrieval_hit_rate_request_validator",
    "RetrievedChunkValidator": "src.evaluation.rag.validators.retrieved_chunk_validator",
    "SemanticSimilarityRequestValidator": "src.evaluation.rag.validators.semantic_similarity_request_validator",
    "TurnRAGResultValidator": "src.evaluation.rag.validators.turn_rag_result_validator",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(name)

    module = import_module(_EXPORTS[name])
    value = getattr(module, name)
    globals()[name] = value
    return value
