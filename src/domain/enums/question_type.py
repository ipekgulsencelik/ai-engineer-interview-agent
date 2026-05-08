from enum import StrEnum


class QuestionType(StrEnum):
    """
    Interview sisteminde desteklenen soru formatlarını temsil eden enum
    modelidir.

    Bu enum interview sırasında kullanılabilecek farklı question pattern'lerini
    standartlaştırır.

    Amaç:
        Sistemde question type kullanımını güvenli, tutarlı ve type-safe hale
        getirmektir.

    Neden question type önemli?
        Çünkü iyi bir teknik interview yalnızca tek tip soru sormamalıdır.

        Farklı question type'lar adayın farklı yetkinliklerini ölçer.

    Örnek:
        conceptual:
            teorik bilgi ölçer

        coding:
            implementation becerisi ölçer

        scenario:
            sistem düşüncesi ve karar verme becerisi ölçer

    Eğer sistem sadece tek tip soru sorarsa:
        - interview monotonlaşır
        - skill coverage düşer
        - adayın bazı güçlü yönleri hiç ölçülemez
        - gerçek mühendislik yetkinliği tam değerlendirilemez

    Bu enum sayesinde sistem:
        ✔ balanced interview flow oluşturabilir
        ✔ question diversity sağlayabilir
        ✔ coverage tracking yapabilir
        ✔ type-aware scoring uygulayabilir
        ✔ adaptive interview strategy geliştirebilir

    Neden Enum kullanıyoruz?
        Çünkü raw string kullanımı:
            - typo riskine
            - inconsistent naming'e
            - invalid state oluşumuna

        yol açabilir.

    Problem örnekleri:
        "concept"
        "Conceptual"
        "code"
        "coding-question"

    gibi tutarsız değerler sistem davranışını bozabilir.

    Enum kullanmanın avantajları:
        ✔ Type safety
        ✔ IDE autocomplete
        ✔ safer refactoring
        ✔ validation kolaylığı
        ✔ domain consistency

    Neden str inheritance kullanıyoruz?
        class QuestionType(str, Enum)

        Bu yapı sayesinde enum değerleri:
            - JSON serialize edilebilir
            - FastAPI/Pydantic ile kolay çalışır
            - database/API işlemlerinde rahat kullanılabilir
            - string karşılaştırmalarında pratik olur

    Kullanım alanları:
        - Question.question_type
        - coverage tracking
        - scoring engine
        - diversity logic
        - analytics
        - interview pacing

    Önemli tasarım notu:
        Bu enum yalnızca desteklenen question type sabitlerini temsil eder.

        Şunları içermez:
            ✘ scoring logic
            ✘ rendering logic
            ✘ evaluation logic
            ✘ UI formatting

        Bu davranışlar ilgili service veya application katmanlarında
        tutulmalıdır.

    Faz-2/Faz-3'te eklenebilecek yeni type'lar:
        - debugging
        - architecture
        - system_design
        - behavioral
        - pair_programming
        - optimization
        - troubleshooting

    Ancak Faz-1 için:
        conceptual
        coding
        scenario

    coverage modeli yeterlidir.

    Example:
        question_type = QuestionType.CODING

        if question_type == QuestionType.CODING:
            print("Run coding evaluation flow")

    Output:
        "Run coding evaluation flow"
    """

    # ---------------------------------------------------------
    # CONCEPTUAL QUESTIONS
    # ---------------------------------------------------------
    # Teorik bilgi ve temel kavram anlayışını ölçen soru tipi.
    #
    # Amaç:
    #   Adayın bir konuyu ne kadar doğru ve derin anladığını görmek.
    #
    # Ölçülen yetkinlikler:
    #   - theoretical understanding
    #   - terminology knowledge
    #   - concept explanation
    #   - abstraction ability
    #
    # Örnek:
    #   - Embedding nedir?
    #   - RAG nasıl çalışır?
    #   - Vector database neden kullanılır?
    #
    # Avantaj:
    #   Hızlı bilgi ölçümü sağlar.
    #
    # Dezavantaj:
    #   Gerçek implementation becerisini tam ölçmez.
    CONCEPTUAL = "conceptual"

    # ---------------------------------------------------------
    # CODING QUESTIONS
    # ---------------------------------------------------------
    # Kod yazma veya implementation odaklı soru tipi.
    #
    # Amaç:
    #   Adayın teorik bilgiyi pratik implementation'a dönüştürme
    #   becerisini ölçmek.
    #
    # Ölçülen yetkinlikler:
    #   - coding skill
    #   - API usage
    #   - algorithmic thinking
    #   - debugging
    #   - software engineering practices
    #
    # Örnek:
    #   - Simple tokenizer implement et
    #   - Embedding retrieval pipeline yaz
    #   - Rate limiter kodla
    #
    # Avantaj:
    #   Gerçek engineering becerisini daha iyi ölçer.
    #
    # Dezavantaj:
    #   Daha fazla süre gerektirir.
    CODING = "coding"

    # ---------------------------------------------------------
    # SCENARIO QUESTIONS
    # ---------------------------------------------------------
    # Gerçek dünya problemi veya sistem tasarımı odaklı soru tipi.
    #
    # Amaç:
    #   Adayın:
    #       - tradeoff analizi
    #       - sistem düşüncesi
    #       - problem çözme yaklaşımı
    #       - architecture reasoning
    #
    # becerilerini ölçmek.
    #
    # Ölçülen yetkinlikler:
    #   - decision making
    #   - architecture thinking
    #   - scalability awareness
    #   - production reasoning
    #   - optimization tradeoffs
    #
    # Örnek:
    #   - Large-scale RAG sistemi nasıl tasarlarsın?
    #   - Retrieval latency problemini nasıl çözersin?
    #   - Hallucination riskini nasıl azaltırsın?
    #
    # Avantaj:
    #   Senior-level düşünce yapısını iyi ölçer.
    #
    # Dezavantaj:
    #   Evaluation daha subjektif olabilir.
    SCENARIO = "scenario"

    SYSTEM_DESIGN = "system_design"
    """
    Büyük ölçekli sistem tasarımı ve mimari odaklı soru tipi.

    Amaç:
        Adayın:
            - high-level architecture design
            - component interaction
            - scalability planning
            - fault tolerance design
            - system tradeoff analysis
        becerilerini ölçmek.

    Ölçülen yetkinlikler:
        - system design thinking
        - architecture reasoning
        - scalability awareness
        - fault tolerance design
        - tradeoff analysis

    Örnek:
        - RAG tabanlı bir arama motoru nasıl tasarlanır?
        - Yüksek trafikli bir RAG sistemi nasıl ölçeklendirilir?
        - RAG sisteminde hata toleransı nasıl sağlanır?
        - RAG sisteminde latency nasıl optimize edilir?
        - RAG sisteminde veri tutarlılığı nasıl sağlanır?

    Avantaj:
        Senior ve mimari odaklı düşünce yapısını iyi ölçer.
        
    Dezavantaj:
        Evaluation daha subjektif olabilir.
    """
