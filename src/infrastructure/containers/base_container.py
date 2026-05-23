from __future__ import annotations

from functools import cached_property


class BaseContainer:
    """
    Base dependency container abstraction.

    Ortak container davranışları için temel sınıf.
    """

    __slots__ = ()