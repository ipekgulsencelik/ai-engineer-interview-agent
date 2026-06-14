from __future__ import annotations

from enum import StrEnum


class ModelStage(
    StrEnum,
):
    """
    Model lifecycle stage.
    """

    DEVELOPMENT = "development"

    VALIDATION = "validation"

    STAGING = "staging"

    CANARY = "canary"

    PRODUCTION = "production"

    ARCHIVED = "archived"