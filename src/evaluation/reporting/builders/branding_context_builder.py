from __future__ import annotations

from src.evaluation.reporting.entities.brand_theme import (
    BrandTheme,
)


class BrandingContextBuilder:
    """
    Builds template/report branding context payloads.
    """

    def build(
        self,
        *,
        theme: BrandTheme,
    ) -> dict[
        str,
        object,
    ]:
        return {
            "theme_id": theme.theme_id,
            "tenant_id": theme.tenant_id,
            "company_name": theme.company_name,
            "theme_name": theme.name,
            "branding_identity": theme.branding_identity,
            "theme_key": theme.theme_key,
            "enabled": theme.enabled,
            "is_default": theme.is_default,
            "colors": {
                "primary": theme.primary_color,
                "secondary": theme.secondary_color,
                "background": theme.background_color,
                "text": theme.text_color,
                "accent": theme.accent_color,
                "muted": theme.muted_color,
                "success": theme.success_color,
                "warning": theme.warning_color,
                "danger": theme.danger_color,
            },
            "fonts": {
                "body": theme.font_family,
                "heading": theme.heading_font_family,
            },
            "logo": {
                "uri": theme.logo_uri,
                "path": theme.logo_path,
            },
            "chart_palette": list(
                theme.chart_palette,
            ),
            "metadata": theme.metadata or {},
        }