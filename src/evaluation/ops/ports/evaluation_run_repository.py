from __future__ import annotations

from abc import ABC

from src.evaluation.ops.repositories.evaluation_run_read_repository import (
    EvaluationRunReadRepository,
)
from src.evaluation.ops.repositories.evaluation_run_write_repository import (
    EvaluationRunWriteRepository,
)


class EvaluationRunRepository(
    EvaluationRunReadRepository,
    EvaluationRunWriteRepository,
    ABC,
):
    """
    Combined repository contract for evaluation runs.

    Use this when a concrete repository supports both
    read and write operations.
    """