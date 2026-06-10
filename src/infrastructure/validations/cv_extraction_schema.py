from __future__ import annotations

from typing import Final

from src.domain.validation.schema_types import (
    ValidationRule,
)


CV_TEXT_RULE: Final[ValidationRule] = {
    "type": str,
    "nullable": False,
    "non_empty": True,
}