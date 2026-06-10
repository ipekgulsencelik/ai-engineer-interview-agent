from __future__ import annotations

from collections.abc import Mapping
from typing import TypeAlias


RawHumanAnnotation: TypeAlias = Mapping[
    str,
    object,
]