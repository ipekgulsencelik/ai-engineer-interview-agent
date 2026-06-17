from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    BOOLEAN_RULE,
    DICT_RULE,
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


BRAND_THEME_SCHEMA: Final[
    SchemaDefinition
] = {
    "theme_id": NON_EMPTY_STRING_RULE,
    "tenant_id": NON_EMPTY_STRING_RULE,
    "company_name": NON_EMPTY_STRING_RULE,
    "name": NON_EMPTY_STRING_RULE,
    "primary_color": NON_EMPTY_STRING_RULE,
    "secondary_color": NON_EMPTY_STRING_RULE,
    "background_color": NON_EMPTY_STRING_RULE,
    "text_color": NON_EMPTY_STRING_RULE,
    "accent_color": OPTIONAL_STRING_RULE,
    "muted_color": OPTIONAL_STRING_RULE,
    "success_color": OPTIONAL_STRING_RULE,
    "warning_color": OPTIONAL_STRING_RULE,
    "danger_color": OPTIONAL_STRING_RULE,
    "font_family": OPTIONAL_STRING_RULE,
    "heading_font_family": OPTIONAL_STRING_RULE,
    "logo_uri": OPTIONAL_STRING_RULE,
    "logo_path": OPTIONAL_STRING_RULE,
    "enabled": BOOLEAN_RULE,
    "is_default": BOOLEAN_RULE,
    "metadata": DICT_RULE,
}