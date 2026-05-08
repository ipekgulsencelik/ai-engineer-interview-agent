from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvaluationResult:
    """
    Aday cevabının evaluation sonucunu temsil eden immutable domain model.

    Bu model interview sisteminde yapılan değerlendirme işleminin
    standartlaştırılmış sonucudur.

    Amaç:
        Evaluation çıktısını:
            - tip güvenli
            - genişletilebilir
            - tutarlı
            - domain odaklı

        bir yapı içerisinde temsil etmektir.

    Neden ayrı model kullanıyoruz?
        Çünkü evaluation sonucu interview sisteminin en kritik domain
        çıktılarından biridir.

        Raw dict kullanımı:
            - typo riskleri oluşturur
            - IDE desteğini azaltır
            - maintainability problemleri yaratır
            - schema consistency'yi bozar

    Örneğin:
        result["feedbak"]
        result["scores"]

        gibi typo hataları runtime'da ortaya çıkar.

    Typed domain model avantajları:
        ✔ type safety
        ✔ IDE autocomplete
        ✔ merkezi validation
        ✔ daha okunabilir API
        ✔ safer refactor
        ✔ immutable state
        ✔ daha güçlü testler

    Neden frozen=True?
        Evaluation sonucu oluşturulduktan sonra değiştirilmemelidir.

        Çünkü evaluation:
            - geçmiş interview state'inin snapshot'ıdır
            - analytics için kullanılabilir
            - audit trail olabilir
            - scoring history'e eklenebilir

        Mutable olması:
            - accidental mutation
            - debugging zorluğu
            - inconsistent history

        riskleri oluşturabilir.

    Bu model hangi alanları içerir?
        score:
            Genel evaluation skoru.

        feedback:
            Aday cevabı hakkında doğal dil geri bildirimi.

        technical_accuracy:
            Teknik doğruluk skoru.

        depth:
            Cevabın derinlik seviyesi.

        communication:
            İfade ve anlatım kalitesi.

        missing_keywords:
            Cevapta eksik bulunan önemli kavramlar.

        follow_up_question:
            Bir sonraki follow-up interview sorusu.

    Kullanım alanları:
        - AnswerEvaluationService
        - InterviewPipeline
        - analytics
        - reporting
        - telemetry
        - adaptive interview flow
        - feedback UI
        - interview history

    Önemli tasarım notu:
        Bu model:
            "evaluation sonucu"

        temsil eder.

        Şunları içermez:
            ✘ LLM raw response
            ✘ provider SDK objeleri
            ✘ HTTP metadata
            ✘ token usage
            ✘ latency bilgisi

        Çünkü bunlar infrastructure concern'dür.

    Gelecekte eklenebilecek alanlar:
        - confidence_score
        - hallucination_risk
        - semantic_coverage
        - rubric_breakdown
        - evaluator_name
        - evaluation_latency
        - reasoning_trace
        - category_scores

    Example:
        result = EvaluationResult(
            score=8.5,
            feedback="Strong understanding of vector retrieval.",
            technical_accuracy=9.0,
            depth=8.0,
            communication=7.5,
        )

        print(result.score)

    Output:
        8.5
    """

    # ---------------------------------------------------------
    # CORE EVALUATION SCORE
    # ---------------------------------------------------------
    # Aday cevabının genel performans skorudur.
    #
    # Beklenen aralık:
    #   0.0 - 10.0
    #
    # Kullanım alanları:
    #   - level transition
    #   - interview analytics
    #   - performance tracking
    #   - adaptive interview flow
    #
    # Örnek:
    #   9.5 -> çok güçlü cevap
    #   7.0 -> iyi cevap
    #   4.0 -> eksik cevap
    #   1.0 -> çok zayıf cevap
    score: float

    # ---------------------------------------------------------
    # NATURAL LANGUAGE FEEDBACK
    # ---------------------------------------------------------
    # Aday cevabı hakkında açıklayıcı geri bildirim.
    #
    # Bu alan:
    #   - UI gösterimi
    #   - candidate feedback
    #   - analytics explanation
    #
    # için kullanılabilir.
    #
    # Örnek:
    #   "Candidate demonstrates strong understanding of retrieval systems."
    feedback: str

    # ---------------------------------------------------------
    # TECHNICAL ACCURACY SCORE
    # ---------------------------------------------------------
    # Cevabın teknik doğruluk seviyesini temsil eder.
    #
    # Ölçülen şey:
    #   - factual correctness
    #   - terminology accuracy
    #   - engineering correctness
    #
    # Örnek:
    #   embedding kavramlarını doğru açıklama
    #   retrieval flow'unu teknik olarak doğru anlatma
    technical_accuracy: float = 0.0

    # ---------------------------------------------------------
    # DEPTH SCORE
    # ---------------------------------------------------------
    # Cevabın yüzeysel mi yoksa derin teknik reasoning içerip
    # içermediğini temsil eder.
    #
    # Ölçülen şey:
    #   - tradeoff analysis
    #   - architectural reasoning
    #   - conceptual depth
    #   - advanced understanding
    #
    # Örnek:
    #   sadece tanım vermek -> düşük depth
    #   optimization/tradeoff anlatmak -> yüksek depth
    depth: float = 0.0

    # ---------------------------------------------------------
    # COMMUNICATION SCORE
    # ---------------------------------------------------------
    # Adayın teknik fikrini ne kadar açık ve anlaşılır ifade ettiğini ölçer.
    #
    # Ölçülen şey:
    #   - clarity
    #   - structure
    #   - explanation quality
    #   - articulation
    #
    # Özellikle senior seviyelerde önemlidir.
    communication: float = 0.0

    # ---------------------------------------------------------
    # MISSING KEYWORDS
    # ---------------------------------------------------------
    # Cevapta eksik kalan önemli teknik kavramları içerir.
    #
    # Kullanım alanları:
    #   - feedback generation
    #   - follow-up question generation
    #   - gap analysis
    #   - analytics
    #
    # field(default_factory=list):
    #   Mutable default problemi oluşmasını engeller.
    #
    # Her instance kendi bağımsız listesini alır.
    missing_keywords: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # FOLLOW-UP QUESTION
    # ---------------------------------------------------------
    # Adayın cevabına göre üretilebilecek bir sonraki interview sorusu.
    #
    # Kullanım alanları:
    #   - adaptive interview
    #   - conversational interview flow
    #   - deep-dive questioning
    #
    # None olabilir.
    #
    # Örnek:
    #   "How would you optimize retrieval latency?"
    follow_up_question: str | None = None

    def __post_init__(self) -> None:
        """
        EvaluationResult oluşturulduktan sonra domain validation kurallarını
        çalıştırır.

        Amaç:
            Geçersiz evaluation state'lerinin sistem içerisine girmesini
            engellemek.

        Şu an doğrulanan kurallar:
            - score 0-10 aralığında olmalı

        Gelecekte eklenebilecek validation'lar:
            - feedback boş olmamalı
            - sub-score'lar 0-10 aralığında olmalı
            - follow_up_question minimum uzunluk kontrolü
            - missing_keywords duplicate kontrolü

        Design Note:
            Validation'ın domain model içerisinde yapılması bilinçlidir.

            Böylece:
                - invalid state erken yakalanır
                - tüm sistem aynı kuralları kullanır
                - infrastructure layer'a bağımlılık azalır
        """

        # ---------------------------------------------------------
        # SCORE VALIDATION
        # ---------------------------------------------------------
        # score yalnızca:
        #   0 <= score <= 10
        #
        # aralığında olmalıdır.
        #
        # Bu validation:
        #   - evaluator bug'larını
        #   - malformed response'ları
        #   - invalid parsing durumlarını
        #
        # erken aşamada yakalar.
        #
        # Örnek invalid değerler:
        #   -1
        #   11
        #   999
        #
        # Bunlar interview pipeline'ı bozabilir.
        if self.score < 0 or self.score > 10:
            raise ValueError("Score must be between 0 and 10.")
