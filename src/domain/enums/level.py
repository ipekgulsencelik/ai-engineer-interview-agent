from enum import StrEnum


class Level(StrEnum):
    """
    Interview sisteminde desteklenen aday ve soru seviyelerini temsil eden
    enum modelidir.

    Bu enum:
        - candidate level
        - question level
        - interview progression
        - scoring logic
        - adaptive difficulty

    gibi sistemin birçok yerinde ortak seviye standardı sağlar.

    Amaç:
        Sistemde string bazlı level kullanımını güvenli ve tutarlı hale
        getirmektir.

    Neden Enum kullanıyoruz?
        Çünkü raw string kullanımı birçok probleme yol açabilir.

        Örnek riskler:
            - typo hataları
            - inconsistent naming
            - invalid state oluşumu
            - runtime bug'ları

        Problem örnekleri:
            "jr"
            "Junior"
            "middle"
            "senior-level"

        gibi değerler sistemde karışıklık yaratabilir.

    Enum kullanmanın avantajları:
        ✔ Type safety sağlar
        ✔ IDE autocomplete desteği verir
        ✔ Invalid value riskini azaltır
        ✔ Domain consistency sağlar
        ✔ Refactor işlemlerini kolaylaştırır
        ✔ Validation logic'i sadeleştirir

    Neden str inheritance kullanıyoruz?
        class Level(str, Enum)

        Bu yapı sayesinde enum değerleri:
            - string gibi davranabilir
            - JSON serialization sırasında kolay kullanılabilir
            - Pydantic/FastAPI ile daha uyumlu çalışır
            - database/API işlemlerinde daha pratik olur

    Örnek:
        Level.JR.value
            → "JR"

        str(Level.MID)
            → "Level.MID"

    Kullanım alanları:
        - Question.level
        - ScoringContext.current_level
        - scoring engine
        - level transition logic
        - filtering
        - analytics
        - interview state

    Level progression sırası:
        JR
            ↓
        MID
            ↓
        SENIOR

    Level anlamları:
        JR:
            Junior-level knowledge.
            Temel kavram bilgisi ve giriş seviyesi problem çözme becerisi.

        MID:
            Mid-level engineering knowledge.
            Gerçek dünya problemleri, sistem düşüncesi ve teknik derinlik.

        SENIOR:
            Senior-level architectural and strategic thinking.
            Scale, tradeoff, optimization ve leadership seviyesinde yaklaşım.

    Tasarım notu:
        Bu enum yalnızca desteklenen level sabitlerini temsil eder.

        Şunları içermez:
            ✘ scoring logic
            ✘ transition logic
            ✘ ordering logic
            ✘ business rules

        Bu davranışlar:
            - LevelTransitionService
            - ScoringEngine
            - helper utility'ler

        içerisinde tutulmalıdır.

    Gelecekte eklenebilecek level'lar:
        - INTERN
        - STAFF
        - PRINCIPAL
        - LEAD
        - ARCHITECT

    Ancak Faz-1 için:
        JR → MID → SENIOR

    progression modeli yeterlidir.

    Example:
        level = Level.JR

        if level == Level.JR:
            print("Junior interview flow")

    Output:
        "Junior interview flow"
    """

    # ---------------------------------------------------------
    # JUNIOR LEVEL
    # ---------------------------------------------------------
    # Entry-level engineering knowledge.
    #
    # Beklenen yetkinlikler:
    #   - temel kavram bilgisi
    #   - giriş seviyesi problem çözme
    #   - basic implementation understanding
    #
    # Örnek:
    #   - Embedding nedir?
    #   - RAG temel akışı nasıl çalışır?
    #   - Vector DB ne işe yarar?
    JR = "JR"

    # ---------------------------------------------------------
    # MID LEVEL
    # ---------------------------------------------------------
    # Intermediate engineering depth.
    #
    # Beklenen yetkinlikler:
    #   - gerçek dünya problem çözme
    #   - tradeoff analizi
    #   - sistem düşüncesi
    #   - production awareness
    #
    # Örnek:
    #   - Retrieval quality nasıl artırılır?
    #   - Embedding modeli nasıl seçilir?
    #   - RAG latency nasıl optimize edilir?
    MID = "MID"

    # ---------------------------------------------------------
    # SENIOR LEVEL
    # ---------------------------------------------------------
    # Advanced architectural and strategic engineering level.
    #
    # Beklenen yetkinlikler:
    #   - large-scale system thinking
    #   - architecture design
    #   - optimization tradeoffs
    #   - leadership-level reasoning
    #
    # Örnek:
    #   - Multi-tenant RAG architecture tasarımı
    #   - Embedding infra scaling strategy
    #   - Evaluation reliability tradeoff'ları
    SENIOR = "SENIOR"
