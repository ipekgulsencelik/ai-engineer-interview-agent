from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class BIColumnInferenceBuilder:
    """
    Infers ordered BI dataset columns from row mappings.
    """

    def infer(
        self,
        *,
        rows: tuple[
            Mapping[
                str,
                Any,
            ],
            ...,
        ],
    ) -> tuple[
        str,
        ...,
    ]:
        columns: list[
            str
        ] = []

        seen: set[
            str
        ] = set()

        for row in rows:
            for key in row.keys():
                if key in seen:
                    continue

                seen.add(
                    key,
                )
                columns.append(
                    key,
                )

        return tuple(
            columns,
        )