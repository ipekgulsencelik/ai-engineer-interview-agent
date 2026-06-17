from __future__ import annotations

from src.evaluation.reporting.entities.brand_theme import (
    BrandTheme,
)


class BrandCSSVariableBuilder:
    """
    Builds CSS variables from brand themes.
    """

    def build(
        self,
        *,
        theme: BrandTheme,
    ) -> dict[
        str,
        str,
    ]:
        variables = {
            "--brand-primary-color": theme.primary_color,
            "--brand-secondary-color": theme.secondary_color,
            "--brand-background-color": theme.background_color,
            "--brand-text-color": theme.text_color,
        }

        if theme.accent_color is not None:
            variables["--brand-accent-color"] = theme.accent_color

        if theme.muted_color is not None:
            variables["--brand-muted-color"] = theme.muted_color

        if theme.success_color is not None:
            variables["--brand-success-color"] = theme.success_color

        if theme.warning_color is not None:
            variables["--brand-warning-color"] = theme.warning_color

        if theme.danger_color is not None:
            variables["--brand-danger-color"] = theme.danger_color

        if theme.font_family is not None:
            variables["--brand-font-family"] = theme.font_family

        if theme.heading_font_family is not None:
            variables["--brand-heading-font-family"] = (
                theme.heading_font_family
            )

        return variables