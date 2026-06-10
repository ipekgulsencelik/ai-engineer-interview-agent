from __future__ import annotations

import pytest

from src.evaluation.metrics.detectors.benchmark_trend_detector import (
    BenchmarkTrendDetector,
)


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ((0.7,), "stable"),
        ((0.7, 0.8), "improving"),
        ((0.8, 0.7), "degrading"),
        ((0.8, 0.7, 0.8), "stable"),
    ],
)
def test_benchmark_trend_detector_should_detect_direction(
    scores: tuple[float, ...],
    expected: str,
) -> None:
    assert BenchmarkTrendDetector.detect(scores=scores) == expected
