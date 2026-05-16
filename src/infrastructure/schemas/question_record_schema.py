from __future__ import annotations

from types import MappingProxyType
from typing import Final


QUESTION_RECORD_SCHEMA: Final = MappingProxyType(
    {
        "id": MappingProxyType(
            {
                "type": str,
                "required": True,
                "non_empty": True,
                "strip": True,
            }
        ),
        "text": MappingProxyType(
            {
                "type": str,
                "required": True,
                "non_empty": True,
                "strip": True,
            }
        ),
        "category": MappingProxyType(
            {
                "type": str,
                "required": True,
                "non_empty": True,
                "strip": True,
            }
        ),
        "level": MappingProxyType(
            {
                "type": str,
                "required": True,
                "non_empty": True,
                "strip": True,
            }
        ),
        "question_type": MappingProxyType(
            {
                "type": str,
                "required": True,
                "non_empty": True,
                "strip": True,
            }
        ),
        "difficulty": MappingProxyType(
            {
                "type": (int, float),
                "required": True,
                "allow_bool": False,
            }
        ),
        "expected_points": MappingProxyType(
            {
                "type": list,
                "required": True,
                "item_type": str,
                "allow_empty": True,
                "strip_items": True,
            }
        ),
        "keywords": MappingProxyType(
            {
                "type": list,
                "required": True,
                "item_type": str,
                "allow_empty": True,
                "strip_items": True,
            }
        ),
        "market_weight": MappingProxyType(
            {
                "type": (int, float),
                "required": True,
                "allow_bool": False,
            }
        ),
        "followup_allowed": MappingProxyType(
            {
                "type": bool,
                "required": True,
            }
        ),
    }
)