from __future__ import annotations

from typing import Any

import mlflow


class MLflowPayloadLogger:
    """
    Logs payload values to MLflow.
    """

    @staticmethod
    def log(
        *,
        payload: dict[str, Any],
    ) -> None:
        for key, value in payload.items():
            if isinstance(
                value,
                int | float,
            ):
                mlflow.log_metric(
                    key,
                    float(value),
                )
            else:
                mlflow.set_tag(
                    f"payload.{key}",
                    str(value),
                )