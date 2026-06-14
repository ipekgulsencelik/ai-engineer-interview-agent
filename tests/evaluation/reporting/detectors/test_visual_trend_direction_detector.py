from __future__ import annotations

from src.evaluation.reporting.detectors.visual_trend_direction_detector import VisualTrendDirectionDetector
from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection


def test_detect_maps_score_sequences_to_direction() -> None:
    assert VisualTrendDirectionDetector.detect(scores=()) == SummaryTrendDirection.UNKNOWN
    assert VisualTrendDirectionDetector.detect(scores=(0.8,)) == SummaryTrendDirection.STABLE
    assert VisualTrendDirectionDetector.detect(scores=(0.6, 0.9)) == SummaryTrendDirection.IMPROVING
    assert VisualTrendDirectionDetector.detect(scores=(0.9, 0.6)) == SummaryTrendDirection.DECLINING
    assert VisualTrendDirectionDetector.detect(scores=(0.8, 0.8)) == SummaryTrendDirection.STABLE
