from __future__ import annotations

from typing import Any

_EXPORTS = {
    "ArtifactVersion": "artifact_version",
    "ExperimentArtifact": "experiment_artifact",
    "ExperimentComparisonResult": "experiment_comparison_result",
    "ExperimentRun": "experiment_run",
    "ExperimentTag": "experiment_tag",
    "ExperimentTrendResult": "experiment_trend_result",
    "LineageEdge": "lineage_edge",
    "ModelRegistryEntry": "model_registry_entry",
    "TrackingEvent": "tracking_event",
    "TrackingProvider": "tracking_provider",
    "WorkerNode": "worker_node",
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(name)

    from importlib import import_module

    module = import_module(
        f"src.evaluation.tracking.entities.{_EXPORTS[name]}",
    )
    value = getattr(module, name)
    globals()[name] = value
    return value
