from __future__ import annotations

from src.evaluation.metrics.engines.evaluator_alignment_engine import (
    EvaluatorAlignmentEngine as CanonicalEvaluatorAlignmentEngine,
)
from src.evaluation.metrics.services.evaluator_alignment_engine import (
    EvaluatorAlignmentEngine,
)


def test_services_evaluator_alignment_engine_should_reexport_canonical_engine() -> None:
    assert EvaluatorAlignmentEngine is CanonicalEvaluatorAlignmentEngine
