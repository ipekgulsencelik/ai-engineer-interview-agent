from __future__ import annotations

import re

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.brand_theme_schema import (
    BRAND_THEME_SCHEMA,
)


class BrandThemeValidator:
    """
    BrandTheme validation service.
    """

    HEX_COLOR_PATTERN = re.compile(
        r"^#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$"
    )

    @classmethod
    def validate(
        cls,
        *,
        theme_id: str,
        tenant_id: str,
        company_name: str,
        name: str,
        primary_color: str,
        secondary_color: str,
        background_color: str,
        text_color: str,
        accent_color: str | None,
        muted_color: str | None,
        success_color: str | None,
        warning_color: str | None,
        danger_color: str | None,
        font_family: str | None,
        heading_font_family: str | None,
        logo_uri: str | None,
        logo_path: str | None,
        enabled: bool,
        is_default: bool,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "theme_id": theme_id,
                "tenant_id": tenant_id,
                "company_name": company_name,
                "name": name,
                "primary_color": primary_color,
                "secondary_color": secondary_color,
                "background_color": background_color,
                "text_color": text_color,
                "accent_color": accent_color,
                "muted_color": muted_color,
                "success_color": success_color,
                "warning_color": warning_color,
                "danger_color": danger_color,
                "font_family": font_family,
                "heading_font_family": (
                    heading_font_family
                ),
                "logo_uri": logo_uri,
                "logo_path": logo_path,
                "enabled": enabled,
                "is_default": is_default,
                "metadata": metadata or {},
            },
            schema=BRAND_THEME_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        cls._validate_color(
            primary_color,
            "primary_color",
        )

        cls._validate_color(
            secondary_color,
            "secondary_color",
        )

        cls._validate_color(
            background_color,
            "background_color",
        )

        cls._validate_color(
            text_color,
            "text_color",
        )

        cls._validate_optional_color(
            accent_color,
            "accent_color",
        )

        cls._validate_optional_color(
            muted_color,
            "muted_color",
        )

        cls._validate_optional_color(
            success_color,
            "success_color",
        )

        cls._validate_optional_color(
            warning_color,
            "warning_color",
        )

        cls._validate_optional_color(
            danger_color,
            "danger_color",
        )

        if (
            logo_uri is not None
            and logo_path is not None
        ):
            raise EvaluationValidationError(
                "logo_uri and logo_path cannot "
                "both be specified."
            )

        if metadata is not None:
            for key, value in metadata.items():
                if (
                    not isinstance(
                        key,
                        str,
                    )
                    or not key.strip()
                ):
                    raise EvaluationValidationError(
                        "metadata keys must be "
                        "non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must "
                        "be strings."
                    )

    @classmethod
    def _validate_color(
        cls,
        value: str,
        field_name: str,
    ) -> None:
        if not cls.HEX_COLOR_PATTERN.match(
            value,
        ):
            raise EvaluationValidationError(
                f"{field_name} must be a valid "
                "hex color code."
            )

    @classmethod
    def _validate_optional_color(
        cls,
        value: str | None,
        field_name: str,
    ) -> None:
        if value is None:
            return

        cls._validate_color(
            value,
            field_name,
        )