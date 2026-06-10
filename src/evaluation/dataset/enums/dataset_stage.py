from __future__ import annotations

from enum import Enum


class DatasetStage(str, Enum):
    """
    Dataset lifecycle stage.
    """

    DEVELOPMENT = "DEVELOPMENT"
    VALIDATION = "VALIDATION"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"

    @property
    def is_active(self) -> bool:
        return self is not DatasetStage.ARCHIVED