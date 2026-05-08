from dataclasses import dataclass


@dataclass(frozen=True)
class FollowUpResult:
    """
    Adaptive follow-up generation sonucunu temsil eden immutable domain model.

    Bu modelin amacı:
        Interview sırasında üretilen adaptive follow-up question çıktısını
        structured ve type-safe şekilde temsil etmektir.

    Follow-up question nedir?
        Follow-up question:
            adayın verdiği cevaba göre dinamik olarak üretilen
            derinleştirici sorudur.

    Amaç:
        Candidate'ın:
            - gerçek bilgi seviyesini
            - reasoning depth'ini
            - teknik hakimiyetini
            - communication yeteneğini

        daha iyi ölçebilmektir.

    Örnek:
        Candidate cevabı:
            "RAG retrieval improves answer quality."

        Follow-up:
            "How would you optimize retrieval latency at scale?"

    Bu yaklaşım sayesinde interview:
        ✔ daha doğal olur
        ✔ daha adaptif olur
        ✔ daha derin teknik analiz sağlar
        ✔ scripted interview hissini azaltır

    Bu model neyi temsil eder?
        ✔ generated follow-up question
        ✔ generation reasoning
        ✔ confidence score

    Bu model ne yapmaz?
        ✘ follow-up generation logic
        ✘ LLM orchestration
        ✘ evaluation
        ✘ retrieval
        ✘ scoring

    Çünkü bu model yalnızca:
        result state representation

    görevi görür.

    Mimari konum:
        FollowUpGenerator
                ↓
        FollowUpResult
                ↓
        Pipeline / UI / API

    Neden frozen=True?
        Çünkü FollowUpResult:
            immutable generation snapshot

        temsil eder.

        Bir follow-up üretildikten sonra:
            - question text
            - confidence
            - reasoning

        değişmemelidir.

        Mutable state:
            - inconsistent orchestration
            - debugging zorluğu
            - concurrency problemleri

        oluşturabilir.

    Confidence neden önemli?
        Çünkü bazı follow-up generation'lar:
            - yüksek semantic confidence
            - düşük ambiguity

        ile oluşurken bazıları:
            - zayıf context
            - düşük semantic certainty

        içerebilir.

        Bu bilgi:
            - UI rendering
            - retry strategy
            - fallback generation
            - orchestration decisions

        için değerlidir.

    Reasoning neden optional?
        Çünkü bazı sistemlerde:
            explainability/debugging

        gerekirken bazı production flow'larında yalnızca generated question
        yeterlidir.

    Kullanım alanları:
        ✔ adaptive interview systems
        ✔ multi-step reasoning interviews
        ✔ conversational AI interviews
        ✔ deep technical screening
        ✔ AI-assisted assessment systems

    Gelecekte eklenebilecek alanlar:
        - follow_up_category
        - semantic_similarity
        - difficulty_adjustment
        - source_question_id
        - reasoning_trace
        - token_usage
        - generation_latency
        - generation_strategy

    Example:
        result = FollowUpResult(
            follow_up_question=(
                "How would you scale vector search?"
            ),
            reasoning=(
                "Candidate mentioned retrieval scaling."
            ),
            confidence=0.91,
        )
    """

    # ---------------------------------------------------------
    # FOLLOW-UP QUESTION
    # ---------------------------------------------------------
    # Candidate'a yöneltilecek adaptive follow-up question text'i.
    #
    # Bu soru genellikle:
    #   - candidate answer
    #   - weak areas
    #   - missing concepts
    #   - semantic gaps
    #
    # dikkate alınarak üretilir.
    #
    # Örnek:
    #   "How would you optimize retrieval latency?"
    #
    # Bu alan zorunludur.
    follow_up_question: str

    # ---------------------------------------------------------
    # GENERATION REASONING
    # ---------------------------------------------------------
    # Follow-up generation reasoning açıklaması.
    #
    # Amaç:
    #   generated follow-up'ın neden üretildiğini açıklamak.
    #
    # Kullanım alanları:
    #   - debugging
    #   - explainability
    #   - telemetry
    #   - evaluator transparency
    #
    # Örnek:
    #   "Candidate demonstrated shallow understanding of embeddings."
    #
    # Optional tutulmuştur çünkü her sistem reasoning göstermek istemeyebilir.
    reasoning: str | None = None

    # ---------------------------------------------------------
    # CONFIDENCE SCORE
    # ---------------------------------------------------------
    # Generated follow-up question'ın güven skoru.
    #
    # Beklenen aralık:
    #   0.0 - 1.0
    #
    # 1.0:
    #   çok yüksek generation confidence
    #
    # 0.0:
    #   çok düşük güven
    #
    # Kullanım alanları:
    #   - fallback generation
    #   - retry strategy
    #   - UI confidence display
    #   - orchestration logic
    #
    # Varsayılan:
    #   0.0
    confidence: float = 0.0

    def __post_init__(self) -> None:
        """
        Domain validation kurallarını çalıştırır.

        Amaç:
            Invalid FollowUpResult state'lerinin sistem içerisine girmesini
            engellemek.

        Doğrulanan kurallar:
            - follow_up_question boş olamaz
            - confidence 0-1 arasında olmalıdır

        Neden validation önemli?
            Çünkü invalid follow-up state:
                - orchestration failure
                - UI rendering problemleri
                - unreliable adaptive flow

            oluşturabilir.

        Design Note:
            Validation domain model seviyesinde yapılır.

            Böylece:
                - invalid state erken yakalanır
                - upper layer sade kalır
                - centralized validation sağlanır
        """

        # ---------------------------------------------------------
        # FOLLOW-UP QUESTION VALIDATION
        # ---------------------------------------------------------
        # Follow-up question boş olamaz.
        #
        # strip():
        #   whitespace-only string'leri de engeller.
        #
        # Çünkü boş follow-up:
        #   anlamsız interview flow oluşturur.
        if not self.follow_up_question.strip():
            raise ValueError("Follow-up question cannot be empty.")

        # ---------------------------------------------------------
        # CONFIDENCE RANGE VALIDATION
        # ---------------------------------------------------------
        # Confidence değeri:
        #   0.0 - 1.0
        #
        # aralığında olmalıdır.
        #
        # Çünkü confidence probabilistic güven seviyesini temsil eder.
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("Confidence must be between 0 and 1.")
