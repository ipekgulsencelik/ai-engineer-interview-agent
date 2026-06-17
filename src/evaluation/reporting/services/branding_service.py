from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.builders.brand_css_variable_builder import (
    BrandCSSVariableBuilder,
)
from src.evaluation.reporting.builders.brand_inline_css_builder import (
    BrandInlineCSSBuilder,
)
from src.evaluation.reporting.builders.branding_context_builder import (
    BrandingContextBuilder,
)
from src.evaluation.reporting.registry.brand_theme_registry import (
    BrandThemeRegistry,
)
from src.evaluation.reporting.validators.brand_theme_default_validator import (
    BrandThemeDefaultValidator,
)
from src.evaluation.reporting.entities.brand_theme import (
    BrandTheme,
)


class BrandingService:
    """
    Application service for tenant-aware branding.
    """

    def __init__(
        self,
        *,
        registry: BrandThemeRegistry,
        default_validator: BrandThemeDefaultValidator,
        css_variable_builder: BrandCSSVariableBuilder,
        inline_css_builder: BrandInlineCSSBuilder,
        context_builder: BrandingContextBuilder,
    ) -> None:
        self._registry = registry
        self._default_validator = default_validator
        self._css_variable_builder = css_variable_builder
        self._inline_css_builder = inline_css_builder
        self._context_builder = context_builder

    def register_theme(
        self,
        *,
        theme: BrandTheme,
    ) -> None:
        self._default_validator.validate(
            theme=theme,
        )

        self._registry.register(
            theme=theme,
        )

    def get_theme(
        self,
        *,
        theme_id: str,
    ) -> BrandTheme | None:
        return self._registry.get(
            theme_id=theme_id,
        )

    def require_theme(
        self,
        *,
        theme_id: str,
    ) -> BrandTheme:
        return self._registry.require(
            theme_id=theme_id,
        )

    def list_themes(
        self,
        *,
        tenant_id: str | None = None,
        enabled_only: bool = True,
    ) -> tuple[
        BrandTheme,
        ...,
    ]:
        themes = self._registry.list()

        if tenant_id is not None:
            themes = tuple(
                theme
                for theme in themes
                if theme.tenant_id == tenant_id
            )

        if enabled_only:
            themes = tuple(
                theme
                for theme in themes
                if theme.enabled
            )

        return themes

    def get_default_theme(
        self,
        *,
        tenant_id: str,
    ) -> BrandTheme | None:
        return self._default_validator.get_default_theme(
            tenant_id=tenant_id,
        )

    def require_default_theme(
        self,
        *,
        tenant_id: str,
    ) -> BrandTheme:
        theme = self.get_default_theme(
            tenant_id=tenant_id,
        )

        if theme is None:
            raise EvaluationValidationError(
                "default brand theme not found.",
            )

        return theme

    def css_variables(
        self,
        *,
        theme_id: str,
    ) -> dict[
        str,
        str,
    ]:
        theme = self.require_theme(
            theme_id=theme_id,
        )

        return self._css_variable_builder.build(
            theme=theme,
        )

    def inline_css(
        self,
        *,
        theme_id: str,
    ) -> str:
        variables = self.css_variables(
            theme_id=theme_id,
        )

        return self._inline_css_builder.build(
            variables=variables,
        )

    def chart_palette(
        self,
        *,
        theme_id: str,
    ) -> tuple[
        str,
        ...,
    ]:
        return self.require_theme(
            theme_id=theme_id,
        ).chart_palette

    def branding_context(
        self,
        *,
        theme_id: str,
    ) -> dict[
        str,
        object,
    ]:
        theme = self.require_theme(
            theme_id=theme_id,
        )

        return self._context_builder.build(
            theme=theme,
        )