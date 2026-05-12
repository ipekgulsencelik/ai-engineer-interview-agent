import pytest

from src.domain.interview.adaptive_pacing import AdaptivePacing
from src.domain.interview.interview_coverage import (
    InterviewCoverage,
)
from src.domain.interview.question_fatigue import (
    QuestionFatigue,
)
from src.domain.retrieval.semantic_relevance import (
    SemanticRelevance,
)
from src.domain.scoring.scoring_signals import ScoringSignals
from src.domain.scoring.scoring_weights import ScoringWeights


def build_signals(**overrides) -> ScoringSignals:
    payload = {
        "coverage": None,
        "fatigue": None,
        "semantic_relevance": None,
        "adaptive_pacing": None,
        "weights": None,
    }

    payload.update(overrides)

    return ScoringSignals(**payload)


def test_scoring_signals_can_be_created_with_defaults() -> None:
    signals = ScoringSignals()

    assert signals.coverage is None
    assert signals.fatigue is None
    assert signals.semantic_relevance is None
    assert signals.adaptive_pacing is None
    assert signals.weights is None


def test_scoring_signals_can_be_created_with_valid_signal_objects() -> None:
    signals = build_signals(
        coverage=InterviewCoverage(),
        fatigue=QuestionFatigue(),
        semantic_relevance=SemanticRelevance(),
        adaptive_pacing=AdaptivePacing(),
        weights=ScoringWeights(),
    )

    assert isinstance(
        signals.coverage,
        InterviewCoverage,
    )

    assert isinstance(
        signals.fatigue,
        QuestionFatigue,
    )

    assert isinstance(
        signals.semantic_relevance,
        SemanticRelevance,
    )

    assert isinstance(
        signals.adaptive_pacing,
        AdaptivePacing,
    )

    assert isinstance(
        signals.weights,
        ScoringWeights,
    )


def test_scoring_signals_is_immutable() -> None:
    signals = ScoringSignals()

    with pytest.raises(Exception):
        signals.weights = ScoringWeights()


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("coverage", object()),
        ("fatigue", "invalid"),
        ("semantic_relevance", 123),
        ("adaptive_pacing", []),
        ("weights", {}),
    ],
)
def test_scoring_signals_rejects_invalid_field_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_signals(
            **{
                field_name: value,
            }
        )