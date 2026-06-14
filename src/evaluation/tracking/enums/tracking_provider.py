from __future__ import annotations

from enum import Enum


class TrackingProvider(
    str,
    Enum,
):
    """
    External tracking providers.
    """

    MLFLOW = "mlflow"

    WANDB = "wandb"