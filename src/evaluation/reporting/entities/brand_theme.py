from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.reporting.validators.brand_theme_validator import (
    BrandThemeValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BrandTheme:
    """
    Immutable tenant-aware brand theme.

    Represents reusable visual branding settings
    for reports, dashboards, exported artifacts,
    templates, and presentation-ready analytics.
    """

    theme_id: str

    tenant_id: str

    company_name: str

    name: str

    primary_color: str

    secondary_color: str

    background_color: str

    text_color: str

    accent_color: str | None = None

    muted_color: str | None = None

    success_color: str | None = None

    warning_color: str | None = None

    danger_color: str | None = None

    font_family: str | None = None

    heading_font_family: str | None = None

    logo_uri: str | None = None

    logo_path: str | None = None

    enabled: bool = True

    is_default: bool = False

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        BrandThemeValidator.validate(
            theme_id=self.theme_id,
            tenant_id=self.tenant_id,
            company_name=self.company_name,
            name=self.name,
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            background_color=self.background_color,
            text_color=self.text_color,
            accent_color=self.accent_color,
            muted_color=self.muted_color,
            success_color=self.success_color,
            warning_color=self.warning_color,
            danger_color=self.danger_color,
            font_family=self.font_family,
            heading_font_family=(
                self.heading_font_family
            ),
            logo_uri=self.logo_uri,
            logo_path=self.logo_path,
            enabled=self.enabled,
            is_default=self.is_default,
            metadata=self.metadata,
        )

    @property
    def has_logo(
        self,
    ) -> bool:
        return (
            self.logo_uri is not None
            or self.logo_path is not None
        )

    @property
    def has_accent_color(
        self,
    ) -> bool:
        return (
            self.accent_color
            is not None
        )

    @property
    def has_fonts(
        self,
    ) -> bool:
        return (
            self.font_family is not None
            or self.heading_font_family
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_custom_theme(
        self,
    ) -> bool:
        return not self.is_default

    @property
    def chart_palette(
        self,
    ) -> tuple[
        str,
        ...,
    ]:
        palette = [
            self.primary_color,
            self.secondary_color,
        ]

        if self.accent_color:
            palette.append(
                self.accent_color,
            )

        if self.success_color:
            palette.append(
                self.success_color,
            )

        if self.warning_color:
            palette.append(
                self.warning_color,
            )

        if self.danger_color:
            palette.append(
                self.danger_color,
            )

        return tuple(
            palette,
        )

    @property
    def branding_identity(
        self,
    ) -> str:
        return (
            f"{self.company_name}"
            f"::{self.name}"
        )

    @property
    def theme_key(
        self,
    ) -> str:
        return (
            f"{self.tenant_id}"
            f":{self.theme_id}"
        )