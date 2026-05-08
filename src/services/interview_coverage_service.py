from src.domain.coverage.interview_coverage import InterviewCoverage
from src.domain.question.question import Question


class InterviewCoverageService:
    """
    Interview boyunca hangi alanların kapsandığını takip eden application
    service.

    Bu service'in temel amacı:
        Interview sürecinde şimdiye kadar hangi:
            - kategorilerin
            - level'ların
            - question type'ların

        kapsandığını analiz etmektir.

    Interview coverage neden önemli?
        Çünkü iyi bir teknik mülakat:
            - yalnızca tek bir konuyu ölçmemelidir
            - balanced skill coverage sağlamalıdır
            - adayın farklı yönlerini değerlendirmelidir

    Örnek problem:
        Eğer sistem sürekli:
            - sadece RAG soruları
            - sadece conceptual sorular
            - sadece MID level sorular

        sorarsa interview dengesiz hale gelir.

    Coverage tracking sayesinde sistem:
        ✔ hangi alanların işlendiğini bilir
        ✔ hangi alanların eksik kaldığını görebilir
        ✔ diversity-aware selection yapabilir
        ✔ tekrar riskini azaltabilir
        ✔ adaptive interview planning yapabilir

    Bu service şu an Faz-1 kapsamında intentionally sade tutulmuştur.

    Şu anda yalnızca:
        - covered categories
        - covered levels
        - covered question types

    bilgilerini üretmektedir.

    Gelecekte eklenebilecek coverage sinyalleri:
        - category distribution percentages
        - weak area coverage
        - semantic diversity coverage
        - difficulty distribution
        - follow-up chain depth
        - interview pacing metrics
        - concept graph traversal
        - unanswered topic detection

    Mimari yaklaşım:
        Bu service yalnızca coverage state üretir.

        Şunları yapmaz:
            ✘ question selection
            ✘ scoring
            ✘ evaluation
            ✘ persistence
            ✘ semantic retrieval

        Böylece Single Responsibility Principle korunur.

    Mimari konum:
        Interview pipeline
                ↓
        InterviewCoverageService
                ↓
        InterviewCoverage

    Neden ayrı service?
        Çünkü coverage calculation:
            - reusable bir use-case'tir
            - selection logic'ten bağımsızdır
            - analytics için tekrar kullanılabilir
            - future telemetry sistemlerinde kullanılabilir

    InterviewCoverage model'i neden ayrı?
        Çünkü coverage interview state'in önemli bir domain snapshot'ıdır.

        Bu snapshot:
            - scoring engine
            - diversity logic
            - analytics
            - UI dashboard
            - recommendation system

        tarafından kullanılabilir.

    Önemli tasarım notu:
        Coverage state immutable snapshot mantığında düşünülmelidir.

        Yani:
            "şu ana kadar interview'de ne kapsandı?"

        sorusunun cevabını temsil eder.

    Örnek:
        covered_categories:
            {
                "RAG",
                "LLM Evaluation",
                "Vector DB"
            }

        covered_levels:
            {
                "JR",
                "MID"
            }

        covered_question_types:
            {
                "conceptual",
                "scenario"
            }
    """

    def build_coverage(
        self,
        asked_questions: list[Question],
    ) -> InterviewCoverage:
        """
        Sorulmuş question listesi üzerinden coverage snapshot oluşturur.

        Bu method interview sırasında şu ana kadar hangi alanların
        kapsandığını hesaplar.

        Akış:
            1. Sorulmuş question'lar alınır
            2. Category coverage çıkarılır
            3. Level coverage çıkarılır
            4. Question type coverage çıkarılır
            5. Immutable InterviewCoverage modeli oluşturulur

        Args:
            asked_questions:
                Interview sırasında daha önce sorulmuş Question listesi.

                Bu liste interview memory/state tarafından tutulabilir.

                Örnek:
                    [
                        Question(category="RAG", ...),
                        Question(category="Vector DB", ...),
                    ]

                Liste boş olabilir.
                Bu durumda boş coverage snapshot üretilir.

        Returns:
            InterviewCoverage:
                Interview coverage snapshot'ını temsil eden immutable domain
                model.

                İçerdiği bilgiler:
                    - covered_categories
                    - covered_levels
                    - covered_question_types

        Design Note:
            Bu method duplicate coverage'ı otomatik olarak elimine eder.

            Çünkü:
                set comprehension kullanılmaktadır.

            Örnek:
                Aynı category'den 10 soru sorulsa bile:
                    covered_categories içinde yalnızca 1 kez görünür.

        Example:
            coverage = service.build_coverage(
                asked_questions=asked_questions
            )

            print(coverage.covered_categories)

        Output:
            {"RAG", "LLM Evaluation"}
        """

        # ---------------------------------------------------------
        # CATEGORY COVERAGE
        # ---------------------------------------------------------
        # Interview boyunca hangi teknik alanların işlendiğini çıkarır.
        #
        # Örnek:
        #   {
        #       "RAG",
        #       "Vector DB",
        #       "Prompt Engineering"
        #   }
        #
        # Set kullanılmasının nedeni:
        #   duplicate category'leri otomatik elimine etmektir.
        #
        # Bu bilgi:
        #   - diversity scoring
        #   - weak area detection
        #   - coverage analytics
        #
        # için kullanılabilir.
        categories = {q.category for q in asked_questions}

        # ---------------------------------------------------------
        # LEVEL COVERAGE
        # ---------------------------------------------------------
        # Interview sırasında hangi difficulty seviyelerinde soru
        # sorulduğunu takip eder.
        #
        # Örnek:
        #   {"JR", "MID"}
        #
        # Bu bilgi:
        #   - adaptive progression
        #   - interview balance
        #   - candidate calibration
        #
        # için kullanılabilir.
        levels = {q.level for q in asked_questions}

        # ---------------------------------------------------------
        # QUESTION TYPE COVERAGE
        # ---------------------------------------------------------
        # Hangi soru formatlarının kullanıldığını takip eder.
        #
        # Örnek:
        #   {
        #       "conceptual",
        #       "coding",
        #       "scenario"
        #   }
        #
        # Bu coverage:
        #   - interview monotony'yi azaltmak
        #   - balanced evaluation yapmak
        #   - farklı skill dimension'larını ölçmek
        #
        # açısından önemlidir.
        question_types = {q.question_type for q in asked_questions}

        # ---------------------------------------------------------
        # COVERAGE SNAPSHOT CREATION
        # ---------------------------------------------------------
        # Toplanan coverage bilgileri immutable InterviewCoverage modeline
        # dönüştürülür.
        #
        # Bu snapshot:
        #   - scoring engine
        #   - analytics
        #   - telemetry
        #   - UI visualization
        #
        # tarafından kullanılabilir.
        #
        # Immutable yapı sayesinde:
        #   - state mutation riskleri azalır
        #   - debugging kolaylaşır
        #   - deterministic behavior korunur
        return InterviewCoverage(
            covered_categories=categories,
            covered_levels=levels,
            covered_question_types=question_types,
        )
