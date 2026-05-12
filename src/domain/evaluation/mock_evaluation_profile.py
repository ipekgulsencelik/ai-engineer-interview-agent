from dataclasses import dataclass, field

from src.domain.constants.evaluation import (
    DEFAULT_CONFIDENCE,
    DEFAULT_MOCK_COMMUNICATION,
    DEFAULT_MOCK_DEPTH,
    DEFAULT_MOCK_FEEDBACK,
    DEFAULT_MOCK_RUBRIC_VERSION,
    DEFAULT_MOCK_SCORE,
    DEFAULT_MOCK_TECHNICAL_ACCURACY,
    MAX_CONFIDENCE,
    MAX_EVALUATION_SCORE,
    MIN_CONFIDENCE,
    MIN_EVALUATION_SCORE,
)


@dataclass(frozen=True)
class MockEvaluationProfile:
    """
    Deterministic mock evaluation davranışını tanımlayan immutable
    configuration/profile domain modelidir.

    Bu modelin temel amacı:
        MockEvaluator için tekrar kullanılabilir, predictable ve
        metadata-driven validation destekli evaluation profile'ı
        sağlamaktır.

    ----------------------------------------------------------------------
    MOCK EVALUATION PROFILE NEDİR?
    ----------------------------------------------------------------------

    MockEvaluationProfile:
        MockEvaluator'ın nasıl evaluation sonucu üreteceğini tanımlar.

    Örneğin:
        - hangi score dönecek
        - hangi feedback üretilecek
        - technical_accuracy ne olacak
        - confidence değeri ne olacak
        - follow-up question üretilecek mi

    gibi deterministic evaluator davranışları bu profile üzerinden
    yönetilir.

    ----------------------------------------------------------------------
    NEDEN AYRI PROFILE MODELİ VAR?
    ----------------------------------------------------------------------

    Eğer mock evaluator behavior'u hard-code edilirse:

        - test senaryoları esnek olmaz
        - farklı evaluation varyasyonları üretmek zorlaşır
        - evaluator büyür
        - reusable fake configuration kaybolur

    Bu nedenle evaluator behavior:
        immutable configuration model ile externalize edilir.

    Böylece:
        - farklı mock senaryoları kolay oluşturulur
        - deterministic test setup sağlanır
        - reusable profile architecture oluşur
        - evaluator sade kalır

    ----------------------------------------------------------------------
    TEST / DEVELOPMENT SENARYOLARI
    ----------------------------------------------------------------------

    Bu model özellikle:

        - unit test
        - integration test
        - local development
        - deterministic QA
        - fake evaluation pipeline
        - API prototyping

    senaryolarında faydalıdır.

    Örnek:

        junior_profile
        senior_profile
        low_confidence_profile
        failing_candidate_profile
        excellent_candidate_profile

    gibi reusable evaluation preset'leri oluşturulabilir.

    ----------------------------------------------------------------------
    IMMUTABILITY
    ----------------------------------------------------------------------

    frozen=True intentional tasarım kararıdır.

    Çünkü evaluation profile:
        runtime sırasında değişmemesi gereken configuration snapshot'ıdır.

    Örneğin:

        profile.score = 999

    gibi accidental mutation'lar engellenmelidir.

    Bunun avantajları:

        - deterministic behavior sağlar
        - thread safety artırır
        - test consistency korur
        - side effect riskini azaltır

    ----------------------------------------------------------------------
    METADATA-DRIVEN VALIDATION
    ----------------------------------------------------------------------

    Validation kuralları:
        field metadata üzerinde declarative şekilde tanımlanır.

    Örnek:

        metadata={
            "finite": True,
            "min_value": 0.0,
            "max_value": 10.0,
        }

    Validator runtime'da bu metadata'yı okuyarak ilgili invariant
    validation'ı uygular.

    Bu yaklaşımın avantajları:

        - self-documenting model sağlar
        - validator generic hale gelir
        - Open/Closed Principle desteklenir
        - field-level invariant görünürlüğü artar

    ----------------------------------------------------------------------
    DOMAIN SAFETY
    ----------------------------------------------------------------------

    Bu model şu invalid state'leri engeller:

        - negative score
        - NaN confidence
        - infinity values
        - empty feedback
        - invalid rubric_version
        - invalid score ranges

    Böylece MockEvaluator:
        her zaman güvenli evaluation profile ile çalışır.

    ----------------------------------------------------------------------
    EXPLAINABILITY
    ----------------------------------------------------------------------

    Bu model yalnızca tek bir score taşımaz.

    Aynı zamanda:

        - technical_accuracy
        - depth
        - communication
        - missing_keywords
        - confidence
        - follow_up_question

    gibi explainable evaluation component'lerini de taşır.

    Bu:
        gerçek evaluator behavior'unu daha iyi simüle etmeyi sağlar.

    ----------------------------------------------------------------------
    BU MODEL NE YAPAR?
    ----------------------------------------------------------------------

    Bu model:

        ✔ deterministic evaluation configuration taşır
        ✔ immutable behavior sağlar
        ✔ metadata-driven validation destekler
        ✔ reusable test profile'ı sağlar
        ✔ explainable evaluation component'leri taşır

    ----------------------------------------------------------------------
    BU MODEL NE YAPMAZ?
    ----------------------------------------------------------------------

    Bu model:

        ✘ evaluation yapmaz
        ✘ scoring hesaplamaz
        ✘ feedback üretmez
        ✘ LLM çağrısı yapmaz
        ✘ persistence işlemi yapmaz

    Sadece:
        mock evaluation configuration snapshot'ı temsil eder.
    """

    score: float = field(
        default=DEFAULT_MOCK_SCORE,
        metadata={
            # Overall evaluation score.
            #
            # Genellikle:
            #   0 - 10
            #
            # aralığında normalize edilmiş mock evaluation score'u temsil eder.
            #
            # Bu score:
            #   - final evaluation sonucu
            #   - candidate overall performance
            #
            # gibi semantic anlam taşır.
            "type": (int, float),

            # NaN / infinity reddedilir.
            #
            # Çünkü:
            #   - analytics bozulabilir
            #   - serialization sorunları oluşabilir
            #   - ranking/evaluation consistency zarar görebilir
            "finite": True,

            # Negatif score semantic olarak geçersizdir.
            "min_value": MIN_NORMALIZED_SCORE,

            # Maksimum mock evaluation score boundary.
            #
            # Burada explicit 10.0 kullanılması:
            #   evaluation domain scale'ini görünür hale getirir.
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    feedback: str = field(
        default=DEFAULT_MOCK_FEEDBACK,
        metadata={
            # Human-readable evaluation feedback.
            #
            # MockEvaluator:
            #   deterministic textual feedback üretebilir.
            #
            # Bu alan:
            #   explainability
            #   UI rendering
            #   API simulation
            # açısından önemlidir.
            "type": str,

            # Empty feedback semantic olarak anlamsızdır.
            #
            # Çünkü evaluator response'unun açıklayıcı olması beklenir.
            "non_empty": True,

            # Leading/trailing whitespace genellikle istenmez.
            #
            # Çünkü evaluator response'unun temiz ve tutarlı olması beklenir.
            "strip": True,  
        },
    )

    technical_accuracy: float = field(
        default=DEFAULT_MOCK_TECHNICAL_ACCURACY,
        metadata={
            # Teknik doğruluk skorudur.
            #
            # Candidate'ın:
            #   factual correctness
            #   engineering accuracy
            #   implementation validity
            #
            # seviyesini temsil eder.
            "type": (int, float),
            "finite": True,
            "min_value": MIN_EVALUATION_SCORE,

            # MAX_NORMALIZED_SCORE genellikle 1.0 olduğu için:
            #
            #   1.0 * 10 = 10
            #
            # elde edilir.
            #
            # Bu yaklaşım:
            #   evaluation scale consistency sağlar.
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    depth: float = field(
        default=DEFAULT_MOCK_DEPTH,
        metadata={
            # Candidate cevabının derinlik seviyesini temsil eder.
            #
            # Örneğin:
            #   yüzeysel cevap mı?
            #   advanced reasoning içeriyor mu?
            #   trade-off analizi var mı?
            #
            # gibi evaluation signal'larını simüle eder.
            "type": (int, float),
            "finite": True,
            "min_value": MIN_EVALUATION_SCORE,
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    communication: float = field(
        default=DEFAULT_MOCK_COMMUNICATION,
        metadata={
            # Candidate'ın communication quality skorudur.
            #
            # Örneğin:
            #   clarity
            #   structure
            #   articulation
            #   readability
            # gibi signal'ları temsil eder.
            "type": (int, float),
            "finite": True,
            "min_value": MIN_EVALUATION_SCORE,
            "max_value": MAX_EVALUATION_SCORE,
        },
    )

    missing_keywords: list[str] = field(
        default_factory=list,
        metadata={
            # Candidate answer'da eksik olduğu düşünülen keyword listesi.
            #
            # Örneğin:
            #   ["vector database", "embedding"]
            #
            # gibi değerler olabilir.
            #
            # default_factory=list kullanımı:
            #   mutable default anti-pattern'ini engeller.
            "type": list,
            "item_type": str,
        },
    )

    follow_up_question: str | None = field(
        default=None,
        metadata={
            # Follow-up interview question.
            #
            # Bazı evaluator senaryolarında:
            #   adaptive interview behavior
            # simüle edilebilir.
            #
            # None olması:
            #   follow-up üretilmediği anlamına gelir.
            "nullable": True,

            # Nullable olsa bile:
            #   None değilse string olmak zorundadır.
            "type": str,
            "strip": True,
        },
    )

    confidence: float = field(
        default=DEFAULT_CONFIDENCE,
        metadata={
            # Evaluator confidence score.
            #
            # Genellikle:
            #   0.0 - 1.0
            #
            # aralığında normalize edilir.
            #
            # Örneğin:
            #   1.0 -> yüksek confidence
            #   0.2 -> düşük confidence
            #
            # semantic anlamı taşır.
            "type": (int, float),
            "finite": True,
            "min_value": MIN_CONFIDENCE,
            "max_value": MAX_CONFIDENCE,
        },
    )

    rubric_version: str = field(
        default=DEFAULT_RUBRIC_VERSION,
        metadata={
            # Evaluation rubric/profile version bilgisi.
            #
            # Özellikle:
            #   testing
            #   analytics
            #   experiment tracking
            #
            # için faydalıdır.
            #
            # Örneğin:
            #   mock-v1
            #   mock-senior-v2
            #   mock-low-confidence-v1
            #
            # gibi profile versiyonları tutulabilir.
            "type": str,

            # Empty rubric version semantic olarak anlamsızdır.
            "non_empty": True,
            "strip": True,
        },
    )

    def __post_init__(self) -> None:
        """
        Dataclass initialization tamamlandıktan sonra invariant
        validation çalıştırılır.

        Validation delegation yaklaşımı kullanılır.

        Böylece:
            - model sade kalır
            - validation reusable olur
            - SRP korunur
            - validator bağımsız test edilebilir

        Validation kapsamında örnek kontroller:

            - score finite mi?
            - confidence 0-1 aralığında mı?
            - feedback boş mu?
            - rubric_version geçerli mi?
            - nullable alanlar doğru çalışıyor mu?
        """

        from src.domain.validators.mock_evaluation_profile_validator import (
            MockEvaluationProfileValidator,
        )

        MockEvaluationProfileValidator.validate(self)