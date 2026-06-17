from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class BISampleRowBuilder:
    """
    Builds sample rows for BI dataset metadata.
    """

    def build(
        self,
        *,
        rows: tuple[
            Mapping[
                str,
                Any,
            ],
            ...,
        ],
        limit: int = 10,
    ) -> tuple[
        dict[
            str,
            Any,
        ],
        ...,
    ]:
        return tuple(
            dict(
                row,
            )
            for row in rows[
                :limit
            ]
        )