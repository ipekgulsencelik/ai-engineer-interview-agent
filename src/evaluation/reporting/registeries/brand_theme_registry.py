from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.entities.brand_theme import (
    BrandTheme,
)


class BrandThemeRegistry:
    """
    In-memory registry for brand themes.
    """

    def __init__(
        self,
        *,
        themes: tuple[
            BrandTheme,
            ...,
        ] = (),
    ) -> None:
        self._themes_by_id: dict[
            str,
            BrandTheme,
        ] = {
            theme.theme_id: theme
            for theme in themes
        }

    def register(
        self,
        *,
        theme: BrandTheme,
    ) -> None:
        if theme.theme_id in self._themes_by_id:
            raise EvaluationValidationError(
                "brand theme already registered.",
            )

        self._themes_by_id[
            theme.theme_id
        ] = theme

    def get(
        self,
        *,
        theme_id: str,
    ) -> BrandTheme | None:
        return self._themes_by_id.get(
            theme_id,
        )

    def require(
        self,
        *,
        theme_id: str,
    ) -> BrandTheme:
        theme = self.get(
            theme_id=theme_id,
        )

        if theme is None:
            raise EvaluationValidationError(
                "brand theme not found.",
            )

        return theme

    def list(
        self,
    ) -> tuple[
        BrandTheme,
        ...,
    ]:
        return tuple(
            self._themes_by_id.values(),
        )