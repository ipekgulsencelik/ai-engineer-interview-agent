from __future__ import annotations

from typing import Final

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    PERCENTAGE_RULE,
    POSITIVE_INTEGER_RULE,
)
from src.domain.validation.schema_types import (
    SchemaDefinition,
)


SAMPLE_ANNOTATION_CONSENSUS_SCHEMA: Final[SchemaDefinition] = {
    "sample_id": NON_EMPTY_STRING_RULE,
    "annotator_count": POSITIVE_INTEGER_RULE,
    "consensus_score": PERCENTAGE_RULE,
    "min_score": PERCENTAGE_RULE,
    "max_score": PERCENTAGE_RULE,
    "score_range": PERCENTAGE_RULE,
}