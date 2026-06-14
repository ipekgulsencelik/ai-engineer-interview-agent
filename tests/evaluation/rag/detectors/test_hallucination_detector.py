from __future__ import annotations

from src.evaluation.rag.detectors.hallucination_detector import HallucinationDetector


def test_hallucination_detector_should_detect_low_faithfulness_as_hallucination() -> None:
    assert HallucinationDetector.detect(faithfulness_score=0.1) is True


def test_hallucination_detector_should_not_detect_high_faithfulness_as_hallucination() -> None:
    assert HallucinationDetector.detect(faithfulness_score=0.9) is False
