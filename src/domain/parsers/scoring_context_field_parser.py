from __future__ import annotations

from src.domain.enums.level import Level


class ScoringContextFieldParser:
    """
    Raw scoring context değerlerini domain-safe değerlere normalize eder.
    """

    @staticmethod
    def parse_level(
        value: Level | str,
    ) -> Level:
        """
        Raw current_level değerini Level enum'una dönüştürür.
        """

        if isinstance(value, Level):
            return value

        try:
            return Level(value)

        except ValueError as exc:
            raise ValueError(
                f"Invalid current level: {value}. "
                f"Expected one of: "
                f"{[level.value for level in Level]}"
            ) from exc