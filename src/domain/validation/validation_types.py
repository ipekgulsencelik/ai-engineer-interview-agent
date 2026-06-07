from __future__ import annotations

from collections.abc import Callable
from typing import TypeAlias


ErrorFactory: TypeAlias = Callable[
    [str],
    Exception,
]