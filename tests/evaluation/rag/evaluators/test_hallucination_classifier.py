from __future__ import annotations

import pytest

from src.evaluation.rag.classifiers.hallucination_classifier import HallucinationClassifier
from src.evaluation.rag.enums.hallucination_label import HallucinationLabel


@pytest.mark.parametrize(
    ("score", "label"),
    [
        (0.0, HallucinationLabel.NONE),
        (0.1, HallucinationLabel.LOW),
        (0.3, HallucinationLabel.MEDIUM),
        (0.6, HallucinationLabel.HIGH),
        (0.9, HallucinationLabel.CRITICAL),
    ],
)
def test_hallucination_classifier_should_map_scores_to_severity_bands(
    score: float,
    label: HallucinationLabel,
) -> None:
    assert HallucinationClassifier.classify(hallucination_score=score) is label
