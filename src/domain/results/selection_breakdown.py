from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.selection_breakdown_validator import (
    SelectionBreakdownValidator,
)


@dataclass(frozen=True)
class SelectionBreakdown:
    """
    Question selection sürecinde üretilen explainable scoring breakdown modelidir.

    Bu modelin temel amacı:
        Selection pipeline içerisinde hesaplanan tüm scoring component'lerini
        immutable ve güvenli bir domain snapshot olarak taşımaktır.

    Bu model özellikle:
        - explainability
        - debugging
        - observability
        - analytics
        - auditability
        - model interpretability

        gibi ihtiyaçlar için kullanılır.

    ----------------------------------------------------------------------
    NEDEN BU MODEL VAR?
    ----------------------------------------------------------------------

    Selection engine genellikle tek bir final score üretir.

    Ancak production-grade AI/interview sistemlerinde yalnızca final score
    yeterli değildir.

    Çünkü sistemin:

        "Neden bu soru seçildi?"

    sorusuna açıklanabilir cevap verebilmesi gerekir.

    Örneğin:

        - level compatibility mi güçlüydü?
        - market demand mi yüksekti?
        - candidate CV gap mi etkili oldu?
        - fatigue reduction mı selection'ı düşürdü?
        - diversity boost mu katkı sağladı?

    gibi sinyallerin ayrı ayrı izlenebilmesi gerekir.

    Bu model bu explainable component'leri taşır.

    ----------------------------------------------------------------------
    IMMUTABILITY (frozen=True)
    ----------------------------------------------------------------------

    Bu model immutable olarak tasarlanmıştır.

    Bunun nedeni:

        Selection sonucu üretildikten sonra
        scoring state'inin değiştirilememesi gerekir.

    Böylece:

        - accidental mutation engellenir
        - thread safety artar
        - debugging kolaylaşır
        - deterministic behavior sağlanır
        - audit consistency korunur

    Örnek:

        breakdown.final_score = 999

    gibi mutation işlemleri runtime'da engellenir.

    ----------------------------------------------------------------------
    NEDEN VALIDATION MODEL İÇİNDE?
    ----------------------------------------------------------------------

    Domain model hiçbir zaman invalid state taşıyamamalıdır.

    Örneğin:

        - NaN
        - infinity
        - negatif score
        - bool masquerading as int
        - 1.7 gibi invalid normalized score

    gibi durumlar domain corruption oluşturur.

    Bu nedenle invariant validation:
        object creation anında çalıştırılır.

    Böylece invalid SelectionBreakdown nesnesi hiçbir zaman
    sistem içine giremez.

    ----------------------------------------------------------------------
    FIELD METADATA ARCHITECTURE
    ----------------------------------------------------------------------

    Validation kuralları doğrudan validator içine hard-code edilmez.

    Bunun yerine her field kendi semantic validation metadata'sını taşır.

    Bu yaklaşımın avantajları:

        1. Validator field isimlerine bağımlı kalmaz
        2. Reflection/introspection desteklenir
        3. Yeni score alanları kolay eklenir
        4. Open/Closed Principle korunur
        5. Validation behavior declarative hale gelir
        6. Model self-describing olur

    Örneğin:

        metadata={
            "normalized": True
        }

    ifadesi şu anlama gelir:

        "Bu alan 0.0-1.0 arasında normalize edilmiş bir score'dur."

    Validator bunu runtime'da metadata üzerinden okuyabilir.

    ----------------------------------------------------------------------
    NORMALIZED SCORE NEDİR?
    ----------------------------------------------------------------------

    normalized=True olan alanlar:

        MIN_NORMALIZED_SCORE <= score <= MAX_NORMALIZED_SCORE

    aralığında olmak zorundadır.

    Genellikle:

        0.0 -> en kötü
        1.0 -> en iyi

    anlamına gelir.

    Bu sistem:
        scoring component'lerinin karşılaştırılabilir
        olmasını sağlar.

    ----------------------------------------------------------------------
    FINAL SCORE NEDİR?
    ----------------------------------------------------------------------

    final_score:
        tüm component'lerin weighted aggregation sonucudur.

    Bu alan:
        normalized olmak zorunda değildir.

    Çünkü weighted scoring sonucunda:

        1.25
        2.7
        4.9

    gibi değerler üretilebilir.

    Bu nedenle:

        allow_above_one=True

    metadata'sı kullanılır.

    Ancak yine de:

        - NaN olamaz
        - infinity olamaz
        - negatif olamaz

    ----------------------------------------------------------------------
    DOMAIN RESPONSIBILITY
    ----------------------------------------------------------------------

    Bu model:

        ✔ scoring sonucu taşır
        ✔ immutable snapshot sağlar
        ✔ explainability verisi sağlar
        ✔ invariant validation çalıştırır

    Bu model:

        ✘ score hesaplamaz
        ✘ ranking yapmaz
        ✘ selection kararı vermez
        ✘ orchestration yönetmez
        ✘ business workflow çalıştırmaz

    Bu ayrım:
        SRP (Single Responsibility Principle)
        açısından kritiktir.
    """

    level_score: float
    market_score: float
    cv_gap_score: float
    difficulty_score: float
    diversity_score: float
    fatigue_score: float
    final_score: float

    def __post_init__(self) -> None:
        """
        Dataclass initialization tamamlandıktan sonra
        domain invariant validation çalıştırılır.

        Amaç:
            Invalid state'in sistem içine girmesini engellemek.

        Validation delegation yaklaşımı kullanılır.

        Bunun nedeni:
            Domain modelin validation implementation detaylarını
            taşımaması ve SRP korunmasıdır.

        Validation logic:
            SelectionBreakdownValidator içinde merkezi olarak yönetilir.

        Böylece:
            - validation reusable olur
            - test edilebilirlik artar
            - model sade kalır
            - validator bağımsız gelişebilir
        """

        SelectionBreakdownValidator.validate(self)