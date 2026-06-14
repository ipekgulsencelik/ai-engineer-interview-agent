from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    OPTIONAL_STRING_RULE,
    TUPLE_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


EXPERIMENT_LINEAGE_GRAPH_SCHEMA: Final[
    SchemaDefinition
] = {
    "graph_id": NON_EMPTY_STRING_RULE,
    "root_experiment_id": NON_EMPTY_STRING_RULE,
    "nodes": TUPLE_RULE,
    "notes": OPTIONAL_STRING_RULE,
}