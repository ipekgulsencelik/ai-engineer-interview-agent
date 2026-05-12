from __future__ import annotations


class EvaluationMetadataNormalizer:
    """
    Raw evaluation metadata değerlerini normalize eder.

    Bu sınıf:
        - validation yapmaz
        - domain model üretmez
        - sadece raw değerleri temizler
    """

    @staticmethod
    def normalize_missing_keywords(
        value: tuple[str, ...] | list[str] | None,
    ) -> tuple[str, ...]:
        if value is None:
            return ()

        normalized_keywords: list[str] = []

        for keyword in value:
            if not isinstance(keyword, str):
                normalized_keywords.append(keyword)  # type: ignore[arg-type]
                continue

            normalized = keyword.strip()

            if normalized:
                normalized_keywords.append(normalized)

        return tuple(
            dict.fromkeys(normalized_keywords),
        )

    @staticmethod
    def normalize_optional_string(
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized = value.strip()

        if not normalized:
            return None

        return normalized