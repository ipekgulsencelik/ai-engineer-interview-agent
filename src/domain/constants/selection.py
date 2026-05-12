"""
Selection domain'ine ait shared business invariant değerleri.

Bu modülün amacı:
    Question selection ve ranking süreçlerinde kullanılan temel
    numeric boundary değerlerini merkezi şekilde yönetmektir.

Bu dosyadaki değerler:
    - magic number kullanımını azaltır
    - domain kurallarını merkezi hale getirir
    - model metadata içinde reuse edilir
    - validator logic'lerini standardize eder
    - değişiklik yönetimini kolaylaştırır

Örneğin:

    rank: int = field(
        metadata={
            "min_value": MIN_RANK,
        }
    )

kullanımı:

    rank: int = field(
        metadata={
            "min_value": 1,
        }
    )

kullanımına göre daha anlamlıdır.

Çünkü MIN_RANK:
    sadece teknik bir sayı değil,
    selection domain'ine ait bir business invariant'tır.

--------------------------------------------------------------------------
NEDEN AYRI CONSTANT MODÜLÜ?
--------------------------------------------------------------------------

Selection domain'inde bazı değerler birçok yerde tekrar kullanılır.

Örneğin:
    - RankedCandidate modeli
    - RankedCandidateValidator
    - SelectionPolicy
    - ranking builder servisleri
    - test dosyaları

Bu değerleri her dosyada hard-code etmek:
    - consistency riskini artırır
    - refactor maliyetini yükseltir
    - domain intent'i gizler
    - testlerde duplication oluşturur

Bu nedenle shared invariant değerleri merkezi bir constant modülünde tutulur.

--------------------------------------------------------------------------
DOMAIN NOTU
--------------------------------------------------------------------------

Bu dosya infrastructure veya application concern değildir.

Buradaki değerler:
    doğrudan selection domain kuralı temsil eder.

Bu yüzden domain katmanı altında konumlandırılması doğrudur.
"""

MIN_RANK = 1
"""
RankedCandidate için izin verilen minimum rank değeridir.

Selection/ranking sistemi 1-based rank mantığı kullanır.

Semantic anlam:

    rank = 1
        En yüksek skorlu / en iyi candidate.

    rank = 2
        İkinci sıradaki candidate.

    rank = 3
        Üçüncü sıradaki candidate.

Bu nedenle:

    rank = 0

geçersiz kabul edilir.

Çünkü 0-based index teknik olarak listeler için anlamlı olabilir,
ancak domain seviyesinde ranking sırası için kafa karıştırıcıdır.

Bu constant özellikle:
    - RankedCandidate metadata'sında
    - RankedCandidateValidator içinde
    - ranking result builder logic'lerinde
    - unit testlerde

reuse edilebilir.
"""

MIN_CANDIDATE_COUNT = 1
"""
Selection/ranking işlemi için gereken minimum candidate sayısını temsil eder.

Selection işlemi, candidate'lar arasından seçim yapmayı amaçlar.

Eğer candidate sayısı 0 ise:
    - selection işlemi anlamsız hale gelir
    - runtime error riski oluşur (örneğin ranked_candidates[0])
    - domain invariant'ı ihlal eder

Bu nedenle minimum candidate count 1 olarak belirlenmiştir.

Bu constant özellikle:
    - SelectionPolicyValidator içinde
    - selection policy'lerin input contract'ında
    - selection process'unun precondition check'lerinde
    - unit testlerde

reuse edilebilir.
"""

MIN_SELECTION_SCORE = 0.0
"""
Selection score için izin verilen minimum değerdir.

Selection score:
    Candidate question'ın selection/ranking sürecindeki
    final veya intermediate numeric değerini temsil eder.

Bu score negatif olmamalıdır.

Neden?
    Çünkü selection score genellikle:
        - relevance strength
        - candidate suitability
        - weighted scoring contribution
        - ranking confidence

    gibi pozitif semantic anlamlar taşır.

Negatif score kullanımı:
    - sorting behavior'ı karmaşıklaştırabilir
    - explainability çıktısını zayıflatabilir
    - selection kararını yorumlamayı zorlaştırabilir
    - analytics/reporting tarafında kafa karıştırabilir

Örnek geçerli değerler:
    0.0
    0.75
    1.0
    2.35
    8.9

Örnek geçersiz değerler:
    -0.1
    -1.0
    -5.4

Not:
    Bu değer score'un maksimum sınırını tanımlamaz.

    Çünkü final selection score weighted aggregation sonucunda
    1.0 üstüne çıkabilir.
"""

MIN_NORMALIZED_SCORE = 0.0
MAX_NORMALIZED_SCORE = 1.0

MIN_FINAL_SCORE = 0.0