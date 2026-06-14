from __future__ import annotations

from src.evaluation.reporting.entities.executive_summary import (
    ExecutiveSummary,
)
from src.evaluation.reporting.utils.json_serialization_utils import (
    JSONSerializationUtils,
)


class ExecutiveSummaryJSONRenderer:
    """
    Renders executive summaries as JSON.
    """

    def __init__(
        self,
        *,
        utils: JSONSerializationUtils | None = None,
    ) -> None:
        self._utils = utils or JSONSerializationUtils()

    def render(
        self,
        *,
        summary: ExecutiveSummary,
    ) -> str:
        return self._utils.to_json(
            payload={
                "summary_id": summary.summary_id,
                "title": summary.title,
                "overall_assessment": summary.overall_assessment,
                "key_findings": list(summary.key_findings),
                "strengths": list(summary.strengths),
                "weaknesses": list(summary.weaknesses),
                "recommendations": list(summary.recommendations),
                "overall_score": summary.overall_score,
                "pass_rate": summary.pass_rate,
                "total_runs": summary.total_runs,
                "average_score": summary.average_score,
                "best_score": summary.best_score,
                "risk_level": summary.risk_level,
                "trend_direction": (
                    None
                    if summary.trend_direction is None
                    else str(summary.trend_direction)
                ),
                "confidence_level": summary.confidence_level,
                "recommendation": summary.recommendation,
                "generated_by": summary.generated_by,
                "notes": summary.notes,
            },
        )