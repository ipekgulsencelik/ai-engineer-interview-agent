"""RAG evaluation package."""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "FaithfulnessEvaluator": "src.evaluation.rag.evaluators.faithfulness_evaluator",
    "RAGEvaluationReport": "src.evaluation.rag.entities.rag_evaluation_report",
    "RAGEvaluationResult": "src.evaluation.rag.value_objects.rag_evaluation_result",
    "RAGEvaluationSample": "src.evaluation.rag.entities.rag_evaluation_sample",
    "RAGSampleEvaluationService": "src.evaluation.rag.services.rag_sample_evaluation_service",
    "RetrievalHitRateEvaluator": "src.evaluation.rag.evaluators.retrieval_hit_rate_evaluator",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(name)

    module = import_module(_EXPORTS[name])
    value = getattr(module, name)
    globals()[name] = value
    return value
