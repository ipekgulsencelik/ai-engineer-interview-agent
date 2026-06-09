from __future__ import annotations

from src.evaluation.metrics.constants.benchmark import (
    ALIGNMENT_WEIGHT,
    CATEGORY_WEIGHT,
)
from src.evaluation.metrics.entities.evaluator_alignment_report import (
    EvaluatorAlignmentReport,
)
from src.evaluation.metrics.value_objects.category_metric_snapshot import (
    CategoryMetricSnapshot,
)

class BenchmarkScoreCalculator:
    """
    Calculates benchmark-level score from global and category metrics.
    """

    @staticmethod
    def calculate(
        *,
        alignment_report: EvaluatorAlignmentReport,
        category_snapshots: tuple[CategoryMetricSnapshot, ...],
    ) -> float:
        if not category_snapshots:
            return (
                alignment_report.overall_alignment_score
            )

        category_score = (
            sum(
                snapshot.overall_alignment_score
                for snapshot in category_snapshots
            )
            / len(category_snapshots, )
        )

        return (
            alignment_report.overall_alignment_score
            * ALIGNMENT_WEIGHT
            + category_score
            * CATEGORY_WEIGHT
        )