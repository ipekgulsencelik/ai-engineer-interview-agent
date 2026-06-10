from __future__ import annotations

import streamlit as st

from src.ui.formatters.evaluation_response_formatter import (
    EvaluationResponseFormatter,
)
from src.ui.schemas.evaluation_response import (
    EvaluationResponse,
)


class ScoreCards:
    """
    Evaluation score visualization component.
    """

    @staticmethod
    def render(
        *,
        evaluation: EvaluationResponse,
    ) -> None:
        metric_items = (
            EvaluationResponseFormatter.to_metric_items(
                evaluation=evaluation,
            )
        )

        columns = st.columns(
            len(metric_items),
        )

        for column, item in zip(
            columns,
            metric_items,
            strict=True,
        ):
            column.metric(
                item.label,
                item.value,
            )