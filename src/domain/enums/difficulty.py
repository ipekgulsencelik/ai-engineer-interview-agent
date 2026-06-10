from __future__ import annotations

from enum import IntEnum


class Difficulty(IntEnum):
    """
    Question difficulty seviyelerini temsil eder.

    EASY:
        Başlangıç seviyesi soru.

    MEDIUM:
        Orta zorlukta soru.

    HARD:
        İleri seviye soru.
    """

    EASY = 1
    MEDIUM = 2
    HARD = 3