import pytest

from src.domain.enums.level import Level
from src.domain.normalizers.level_normalizer import DefaultLevelNormalizer


def test_normalize_accepts_level_enum() -> None:
    normalizer = DefaultLevelNormalizer()

    assert normalizer.normalize(Level.JR) == Level.JR


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("JR", Level.JR),
        ("MID", Level.MID),
        ("SENIOR", Level.SENIOR),
        ("  MID ", Level.MID),
    ],
)
def test_normalize_accepts_valid_level_strings(value: str, expected: Level) -> None:
    normalizer = DefaultLevelNormalizer()

    assert normalizer.normalize(value) == expected


@pytest.mark.parametrize("value", ["", "beginner", "mid", None, 123])
def test_normalize_rejects_invalid_values(value: object) -> None:
    normalizer = DefaultLevelNormalizer()

    with pytest.raises(ValueError, match="Invalid current level"):
        normalizer.normalize(value)  # type: ignore[arg-type]