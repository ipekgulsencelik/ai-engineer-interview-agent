from __future__ import annotations

from typing import Any

import wandb


class WandBRunInitializer:
    """
    Initializes W&B runs.
    """

    def __init__(
        self,
        *,
        project: str,
        entity: str | None = None,
        group: str | None = None,
        job_type: str | None = None,
        mode: str | None = None,
    ) -> None:
        self._project = project
        self._entity = entity
        self._group = group
        self._job_type = job_type
        self._mode = mode

    def init(
        self,
        *,
        name: str,
        tags: tuple[str, ...] = (),
        config: dict[str, Any] | None = None,
    ):
        return wandb.init(
            project=self._project,
            entity=self._entity,
            group=self._group,
            job_type=self._job_type,
            mode=self._mode,
            name=name,
            tags=list(tags),
            config=config or {},
            reinit=True,
        )