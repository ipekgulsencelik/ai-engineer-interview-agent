from __future__ import annotations

from typing import Annotated

from pydantic import Field
from pydantic import StringConstraints

from src.api.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)


NonEmptyString = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
    ),
]


Score = Annotated[
    float,
    Field(
        ge=MIN_EVALUATION_SCORE,
        le=MAX_EVALUATION_SCORE,
    ),
]


PositiveFloat = Annotated[
    float,
    Field(
        gt=0.0,
    ),
]