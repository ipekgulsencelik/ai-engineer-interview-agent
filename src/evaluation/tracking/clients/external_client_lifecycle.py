from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ExternalClientLifecycle(
    ABC,
):
    """
    Client port for external integration lifecycle.
    """

    @abstractmethod
    async def close(
        self,
    ) -> None:
        """
        Closes client resources.
        """