from __future__ import annotations

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.registeries.brand_theme_registry import (
    BrandThemeRegistry,
)
from src.evaluation.reporting.entities.brand_theme import (
    BrandTheme,
)


class BrandThemeDefaultValidator:
    """
    Validates tenant default theme constraints.
    """

    def __init__(
        self,
        *,
        registry: BrandThemeRegistry,
    ) -> None:
        self._registry = registry

    def validate(
        self,
        *,
        theme: BrandTheme,
    ) -> None:
        if not theme.is_default:
            return

        existing_default = self.get_default_theme(
            tenant_id=theme.tenant_id,
        )

        if existing_default is not None:
            raise EvaluationValidationError(
                "tenant already has a default brand theme.",
            )

    def get_default_theme(
        self,
        *,
        tenant_id: str,
    ) -> BrandTheme | None:
        for theme in self._registry.list():
            if (
                theme.tenant_id == tenant_id
                and theme.enabled
                and theme.is_default
            ):
                return theme

        return None