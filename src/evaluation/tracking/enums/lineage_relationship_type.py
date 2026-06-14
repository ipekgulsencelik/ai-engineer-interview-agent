from __future__ import annotations

from enum import StrEnum


class LineageRelationshipType(
    StrEnum,
):
    """
    Lineage relationship type.
    """

    DERIVED_FROM = "derived_from"

    RETRAINED_FROM = "retrained_from"

    FINETUNED_FROM = "finetuned_from"

    DATASET_UPDATED = "dataset_updated"

    BENCHMARK_UPDATED = "benchmark_updated"

    CONFIG_UPDATED = "config_updated"

    MODEL_UPDATED = "model_updated"

    EVALUATOR_UPDATED = "evaluator_updated"

    MANUAL_LINK = "manual_link"