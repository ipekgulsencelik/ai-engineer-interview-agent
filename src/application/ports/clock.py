from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """
    Time provider contract.
    """

    @abstractmethod
    def now(self) -> datetime:
        """
        Current datetime döndürür.
        """
        ...