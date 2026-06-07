from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetValidationResult:
    """
    Dataset validation result.

    Bu entity:
        - dataset'in geçerli olup olmadığını
        - bulunan hata listesini
        - bulunan uyarı listesini

    immutable snapshot olarak taşır.
    """

    is_valid: bool

    errors: list[str]

    warnings: list[str]