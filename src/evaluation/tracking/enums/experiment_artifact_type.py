from __future__ import annotations

from enum import StrEnum


class ExperimentArtifactType(
    StrEnum,
):
    """
    Experiment artifact type.
    """

    REPORT = "report"

    METRICS = "metrics"

    DATASET = "dataset"

    PLOT = "plot"

    LOG = "log"

    MODEL_CARD = "model_card"

    AUDIT = "audit"

    EXPORT = "export"

    CONFIG = "config"

    OTHER = "other"