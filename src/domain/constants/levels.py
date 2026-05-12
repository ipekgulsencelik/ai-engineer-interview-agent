from src.domain.enums.level import Level


"""
Interview system içerisindeki resmi level progression sırası.

Bu sıra:
    - level up/down işlemlerinde
    - progression traversal'da
    - boundary kontrollerinde
    - transition policy içinde

kullanılır.

Progression:
    JR -> MID -> SENIOR

Not:
    Bu sıra business-critical'dir.

    Çünkü transition algoritması:
        current_index +/- 1

    mantığıyla çalışır.

İleride:
    STAFF
    PRINCIPAL

gibi seviyeler eklenirse
yalnızca bu liste güncellenir.
"""

LEVEL_ORDER = [
    Level.JR,
    Level.MID,
    Level.SENIOR,
]