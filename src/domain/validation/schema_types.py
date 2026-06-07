from __future__ import annotations

from typing import TypeAlias

from src.domain.validation.schema_rules import (
    ValidationRule,
)


ValidationSchema: TypeAlias = dict[str, ValidationRule]
SchemaDefinition: TypeAlias = ValidationSchema