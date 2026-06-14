from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.enums.lineage_relationship_type import (
    LineageRelationshipType,
)
from src.evaluation.tracking.validators.lineage_edge_validator import (
    LineageEdgeValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class LineageEdge:
    """
    Immutable lineage edge.

    Represents a directed parent-child relationship
    between two experiment lineage nodes.
    """

    edge_id: str

    parent_id: str

    child_id: str

    relationship_type: LineageRelationshipType

    created_at: datetime

    description: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        LineageEdgeValidator.validate(
            edge_id=self.edge_id,
            parent_id=self.parent_id,
            child_id=self.child_id,
            relationship_type=self.relationship_type,
            created_at=self.created_at,
            description=self.description,
            metadata=self.metadata,
        )

    @property
    def is_self_reference(
        self,
    ) -> bool:
        return (
            self.parent_id
            == self.child_id
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )