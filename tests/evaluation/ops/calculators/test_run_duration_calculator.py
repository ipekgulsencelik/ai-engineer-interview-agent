from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.evaluation.ops.calculators.run_duration_calculator import RunDurationCalculator


def test_run_duration_calculator_should_return_elapsed_seconds() -> None:
    started_at = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    completed_at = datetime(2026, 1, 1, 0, 0, 1, 250000, tzinfo=timezone.utc)

    assert RunDurationCalculator.calculate(
        started_at=started_at,
        completed_at=completed_at,
    ) == pytest.approx(1.25)
