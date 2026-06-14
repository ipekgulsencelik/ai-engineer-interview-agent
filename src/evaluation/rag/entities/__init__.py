"""RAG entities."""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "ExperimentLineageGraph": "src.evaluation.rag.entities.experiment_lineage_graph",
    "ExperimentNode": "src.evaluation.rag.entities.experiment_node",
    "RAGDatasetRunResult": "src.evaluation.rag.entities.rag_dataset_run_result",
    "RAGEvaluationReport": "src.evaluation.rag.entities.rag_evaluation_report",
    "RAGEvaluationSample": "src.evaluation.rag.entities.rag_evaluation_sample",
    "RetrievedChunk": "src.evaluation.rag.entities.retrieved_chunk",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(name)

    module = import_module(_EXPORTS[name])
    value = getattr(module, name)
    globals()[name] = value
    return value
