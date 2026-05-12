from src.domain.entities.question import Question


class MockEvaluatorValidator:
    """
    MockEvaluator input validation kurallarını yöneten validator sınıfıdır.

    Bu validator'ın temel amacı:
        MockEvaluator evaluation pipeline'ına giren input değerlerinin
        güvenli, tutarlı ve beklenen domain contract'lara uygun olduğunu
        garanti etmektir.

    ----------------------------------------------------------------------
    MOCK EVALUATOR NEDİR?
    ----------------------------------------------------------------------

    MockEvaluator genellikle:

        - test ortamlarında
        - local development süreçlerinde
        - deterministic evaluation senaryolarında
        - integration bağımlılıklarını izole etmek için

    kullanılan lightweight evaluator implementasyonudur.

    Gerçek LLM veya ML evaluator yerine:
        predictable/deterministic evaluation sonucu üretir.

    Örneğin:

        {
            "score": 7,
            "feedback": "Good answer.",
        }

    gibi mock response'lar döndürebilir.

    ----------------------------------------------------------------------
    NEDEN AYRI VALIDATOR VAR?
    ----------------------------------------------------------------------

    MockEvaluator'ın sorumluluğu:
        evaluation result üretmektir.

    Validation logic evaluator içine gömülürse:

        - evaluator büyür
        - SRP zayıflar
        - validation tekrarları oluşabilir
        - test etmek zorlaşır

    Bu nedenle validation ayrı sınıfa alınır.

    Böylece:
        - evaluator sade kalır
        - reusable validation logic oluşur
        - fail-fast behavior sağlanır
        - validation centralized olur

    ----------------------------------------------------------------------
    VALIDATION KAPSAMI
    ----------------------------------------------------------------------

    Bu validator iki temel input'u validate eder:

        1. question
            Evaluation yapılacak Question domain entity'si.

        2. answer
            Candidate tarafından verilen textual answer.

    ----------------------------------------------------------------------
    NEDEN QUESTION TYPE VALIDATION KRİTİK?
    ----------------------------------------------------------------------

    Evaluator:
        Question entity'si üzerinden çalışır.

    Çünkü evaluator genellikle:
        - question.text
        - expected_points
        - category
        - level
        - difficulty

    gibi domain alanlarına ihtiyaç duyar.

    Eğer yanlış tip verilirse:

        question = {}
        question = "What is RAG?"
        question = None

    evaluator runtime'da başarısız olabilir.

    Bu nedenle explicit type validation uygulanır.

    ----------------------------------------------------------------------
    NEDEN EMPTY ANSWER REDDEDİLİYOR?
    ----------------------------------------------------------------------

    Evaluation semantic olarak:
        candidate response'u değerlendirme işlemidir.

    Eğer answer boşsa:

        ""
        "   "

    gibi değerler meaningful evaluation üretmez.

    Bu nedenle:
        boş answer invalid state kabul edilir.

    ----------------------------------------------------------------------
    DEFENSIVE DOMAIN PROGRAMMING
    ----------------------------------------------------------------------

    Python dynamically typed olduğu için runtime'da invalid input
    evaluator pipeline'ına girebilir.

    Örneğin:

        answer = None
        answer = 123
        answer = []
        question = object()

    gibi durumlar mümkündür.

    Bu validator:
        invalid evaluation state'in evaluator logic'ine ulaşmasını engeller.

    ----------------------------------------------------------------------
    DESIGN PRINCIPLES
    ----------------------------------------------------------------------

    Bu validator şu prensipleri destekler:

        - fail-fast validation
        - SRP
        - explicit domain contracts
        - reusable validation logic
        - clean evaluator implementation

    ----------------------------------------------------------------------
    BU VALIDATOR NE YAPMAZ?
    ----------------------------------------------------------------------

    Bu validator:

        ✘ evaluation yapmaz
        ✘ scoring hesaplamaz
        ✘ feedback üretmez
        ✘ LLM çağrısı yapmaz
        ✘ persistence işlemi yapmaz

    Sadece:
        evaluator input safety sağlar.
    """

    @staticmethod
    def validate_question(
        question: Question,
    ) -> None:
        """
        Evaluation yapılacak Question nesnesini validate eder.

        ------------------------------------------------------------------
        VALIDATION KURALI
        ------------------------------------------------------------------

        question:
            geçerli Question domain entity'si olmalıdır.

        ------------------------------------------------------------------
        NEDEN QUESTION ENTITY GEREKLİ?
        ------------------------------------------------------------------

        Evaluator logic'i genellikle question metadata'sına ihtiyaç duyar.

        Örneğin:
            - question.text
            - expected_points
            - difficulty
            - category

        gibi alanlar evaluation sırasında kullanılabilir.

        Bu nedenle evaluator:
            primitive veri yerine doğrudan Question entity'si bekler.

        ------------------------------------------------------------------
        FAIL-FAST YAKLAŞIMI
        ------------------------------------------------------------------

        Eğer invalid question evaluator logic'ine ulaşırsa:
            daha belirsiz runtime exception oluşabilir.

        Bu validator:
            problemi erken aşamada ve anlamlı hata mesajıyla yakalar.

        ------------------------------------------------------------------
        Args
        ------------------------------------------------------------------

        question:
            Evaluation yapılacak Question domain entity'si.

        ------------------------------------------------------------------
        Raises
        ------------------------------------------------------------------

        TypeError:
            question geçerli Question instance'ı değilse.
        """

        if not isinstance(question, Question):
            raise TypeError(
                "question must be a Question instance."
            )

    @staticmethod
    def validate_answer(
        answer: str,
    ) -> None:
        """
        Candidate answer input'unu validate eder.

        Validation kuralları:

            1. answer string olmalıdır
            2. answer boş olmamalıdır

        ------------------------------------------------------------------
        NEDEN STRING VALIDATION VAR?
        ------------------------------------------------------------------

        Evaluator textual response değerlendirmek için tasarlanmıştır.

        Bu nedenle:

            answer = 123
            answer = []
            answer = {}
            answer = None

        gibi değerler semantic olarak geçersizdir.

        ------------------------------------------------------------------
        NEDEN EMPTY ANSWER REDDEDİLİYOR?
        ------------------------------------------------------------------

        Evaluation meaningful textual content gerektirir.

        Şu değerler:
            ""
            "   "

        semantic olarak "cevap verilmedi" anlamına gelir.

        Bu durumda:
            evaluator çalıştırmak anlamsız olabilir.

        Bu nedenle:
            empty answer fail-fast şekilde reddedilir.

        ------------------------------------------------------------------
        strip() NEDEN KULLANILIYOR?
        ------------------------------------------------------------------

        Kullanıcı yalnızca whitespace gönderebilir:

            "     "
            "\\n"
            "\\t"

        Bu değerler teknik olarak empty string değildir.

        Ancak semantic olarak boş cevaptır.

        strip() kullanımı:
            whitespace-only input'ları da reddeder.

        ------------------------------------------------------------------
        Args
        ------------------------------------------------------------------

        answer:
            Candidate tarafından verilen textual answer.

        ------------------------------------------------------------------
        Raises
        ------------------------------------------------------------------

        TypeError:
            answer string değilse.

        ValueError:
            answer boş veya yalnızca whitespace ise.
        """

        if not isinstance(answer, str):
            raise TypeError(
                "answer must be a string."
            )

        if not answer.strip():
            raise ValueError(
                "answer cannot be empty or whitespace only."
            )