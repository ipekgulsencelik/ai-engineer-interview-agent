import pytest

from src.domain.enums.level import Level
from src.domain.scoring.scoring_context import ScoringContext
from src.domain.scoring.scoring_signals import ScoringSignals


def build_context(**overrides) -> ScoringContext:
    payload = {
        "current_level": Level.JR,
        "cv_skills": [],
        "asked_question_ids": [],
        "recent_scores": [],
        "weak_areas": [],
        "signals": ScoringSignals(),
    }

    payload.update(overrides)

    return ScoringContext(**payload)


def test_scoring_context_can_be_created_with_valid_values() -> None:
    context = build_context()

    assert context.current_level == Level.JR
    assert context.cv_skills == []
    assert context.asked_question_ids == []
    assert context.recent_scores == []
    assert context.weak_areas == []
    assert isinstance(
        context.signals,
        ScoringSignals,
    )


def test_scoring_context_parses_string_level() -> None:
    context = build_context(
        current_level="MID",
    )

    assert context.current_level == Level.MID


def test_scoring_context_is_immutable() -> None:
    context = build_context()

    with pytest.raises(Exception):
        context.current_level = Level.SENIOR


@pytest.mark.parametrize(
    "value",
    [
        "INVALID",
        "expert",
        "",
    ],
)
def test_scoring_context_rejects_invalid_level(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Invalid current level",
    ):
        build_context(
            current_level=value,
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("cv_skills", "python"),
        ("asked_question_ids", {}),
        ("recent_scores", "7.5"),
        ("weak_areas", object()),
        ("signals", {}),
    ],
)
def test_scoring_context_rejects_invalid_field_types(
    field_name: str,
    value,
) -> None:
    with pytest.raises(TypeError):
        build_context(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("cv_skills", ["", "RAG"]),
        ("asked_question_ids", ["q1", ""]),
        ("weak_areas", ["", "System Design"]),
    ],
)
def test_scoring_context_rejects_empty_string_items(
    field_name: str,
    value: list[str],
) -> None:
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        build_context(
            **{
                field_name: value,
            }
        )


@pytest.mark.parametrize(
    "value",
    [
        [7.0, float("inf")],
        [7.0, float("-inf")],
        [7.0, float("nan")],
    ],
)
def test_scoring_context_rejects_non_finite_recent_scores(
    value: list[float],
) -> None:
    with pytest.raises(
        ValueError,
        match="Items in recent_scores must be finite",
    ):
        build_context(
            recent_scores=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        [-1.0],
        [11.0],
    ],
)
def test_scoring_context_rejects_invalid_recent_score_range(
    value: list[float],
) -> None:
    with pytest.raises(ValueError):
        build_context(
            recent_scores=value,
        )


def test_scoring_context_rejects_bool_values_in_recent_scores() -> None:
    with pytest.raises(TypeError):
        build_context(
            recent_scores=[True],
        )