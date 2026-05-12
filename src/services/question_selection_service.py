from src.domain.question.question import Question
from src.domain.scoring.scoring_context import ScoringContext
from src.interfaces.scoring_engine import ScoringEngine
from src.domain.filter.candidate_filter import (
    CandidateFilter,
)


class QuestionSelectionService:
    """
    Candidate question listesi içerisinden mevcut interview context'i için
    en uygun soruyu seçen application service.

    Bu service'in temel sorumluluğu:
        - kullanılabilir soruları filtrelemek
        - her soruya skor hesaplatmak
        - en yüksek skorlu soruyu seçmek

    Sistem neden ayrı bir selection service kullanıyor?
        Çünkü question selection interview sisteminin en kritik orchestration
        kararlarından biridir.

        Soru seçimi:
            - candidate experience
            - interview adaptivity
            - topic coverage
            - difficulty progression
            - evaluation quality

        üzerinde doğrudan etkiye sahiptir.

    Bu service ne yapar?
        ✔ Daha önce sorulmuş soruları filtreler
        ✔ Candidate question pool oluşturur
        ✔ Her soru için scoring engine çağırır
        ✔ En uygun soruyu seçer

    Bu service ne yapmaz?
        ✘ scoring algoritmasını implemente etmez
        ✘ evaluator çağırmaz
        ✘ persistence işlemi yapmaz
        ✘ semantic embedding üretmez
        ✘ level transition yönetmez

    Böylece Single Responsibility Principle korunur.

    Mimari yaklaşım:
        Bu service scoring algoritmasını bilmez.

        Bunun yerine yalnızca:
            ScoringEngine abstraction'ına bağımlıdır.

        Bu yaklaşım sayesinde:
            - scoring algoritması değişebilir
            - selection logic stabil kalır
            - test edilebilirlik artar
            - farklı ranking stratejileri desteklenebilir

    Örnek scoring engine implementasyonları:
        - WeightedScoringEngine
        - RuleBasedScoringEngine
        - DiversityAwareScoringEngine
        - AdaptiveDifficultyScoringEngine
        - SemanticCoverageScoringEngine

    Dependency Injection:
        Scoring engine constructor üzerinden inject edilir.

        Böylece:
            - Loose coupling sağlanır
            - Testlerde fake scoring engine kullanılabilir
            - Algoritma değişimi kolaylaşır

    Örnek:
        service = QuestionSelectionService(
            scoring_engine=WeightedScoringEngine()
        )

    Mimari konum:
        Presentation Layer:
            CLI / API / UI

                ↓

        Application Layer:
            QuestionSelectionService

                ↓

        Interface:
            ScoringEngine

                ↓

        Infrastructure / Domain Logic:
            WeightedScoringEngine

    Question selection neden önemli?
        Kötü selection:
            - aynı kategoride tekrar üretir
            - aday seviyesine uygun olmayan soru seçer
            - interview'i monoton hale getirir
            - coverage problemleri oluşturur

        İyi selection:
            - adaptif interview sağlar
            - weak area exploration yapar
            - balanced topic distribution üretir
            - gerçek teknik derinlik ölçebilir

    Faz-1 yaklaşımı:
        Şu an seçim mantığı intentionally basit tutulmuştur.

        Akış:
            1. Asked question'ları filtrele
            2. Kalan sorular için skor hesapla
            3. En yüksek skorlu soruyu seç

    Gelecekte eklenebilecek gelişmiş özellikler:
        - semantic diversity filtering
        - category balancing
        - fatigue prevention
        - stochastic exploration
        - exploration vs exploitation
        - memory graph traversal
        - multi-objective optimization
        - reranking pipeline
        - interview pacing

    Önemli tasarım notu:
        Selection logic ile scoring logic ayrılmıştır.

        Çünkü:
            selection:
                orchestration problemidir

            scoring:
                ranking problemidir

        Bu ayrım sistemin maintainability'sini ciddi şekilde artırır.
    """

    def __init__(self, scoring_engine: ScoringEngine) -> None:
        """
        QuestionSelectionService instance'ı oluşturur.

        Args:
            scoring_engine:
                Soruların uygunluk skorunu hesaplayacak scoring engine
                implementasyonudur.

                Service doğrudan belirli bir algoritmaya bağımlı değildir.

                Bunun yerine yalnızca:
                    ScoringEngine abstraction'ını bilir.

                Bu sayede:
                    - farklı scoring stratejileri kolayca değiştirilebilir
                    - testlerde mock engine kullanılabilir
                    - service daha modüler hale gelir

        Example:
            service = QuestionSelectionService(
                scoring_engine=WeightedScoringEngine()
            )

        Test Example:
            service = QuestionSelectionService(
                scoring_engine=MockScoringEngine()
            )
        """

        # ---------------------------------------------------------
        # DEPENDENCY INJECTION
        # ---------------------------------------------------------
        # Service scoring algoritmasını kendi oluşturmaz.
        #
        # Böylece:
        #   - loose coupling korunur
        #   - dependency inversion uygulanır
        #   - scoring logic değişebilir hale gelir
        self.scoring_engine = scoring_engine

    def select_question(
        self,
        questions: list[Question],
        context: ScoringContext,
    ) -> Question:
        """
        Candidate question listesi içerisinden mevcut context için en uygun
        soruyu seçer.

        Selection akışı:
            1. Daha önce sorulmuş sorular filtrelenir.
            2. Kullanılabilir soru havuzu oluşturulur.
            3. Her soru scoring engine ile skorlanır.
            4. En yüksek skorlu soru seçilir.

        Args:
            questions:
                Aday soru havuzudur.

                Bu liste genellikle repository veya retrieval katmanından gelir.

                Her Question:
                    - category
                    - level
                    - difficulty
                    - market_weight
                    - question_type

                gibi selection için kritik metadata içerir.

            context:
                Mevcut interview durumunu temsil eden scoring context'tir.

                Bu context genellikle:
                    - current_level
                    - asked_question_ids
                    - recent_scores
                    - weak_areas
                    - cv_skills
                    - coverage state

                gibi bilgileri içerir.

                Scoring engine bu context'i kullanarak adaptive ranking yapar.

        Returns:
            Question:
                Mevcut interview context'i için en uygun soru.

                Bu soru:
                    - daha önce sorulmamış
                    - scoring engine tarafından yüksek skor almış
                    - mevcut interview state ile uyumlu

                bir soru olacaktır.

        Raises:
            ValueError:
                Kullanılabilir soru kalmamışsa fırlatılır.

                Örnek:
                    - tüm sorular zaten sorulmuşsa
                    - input listesi boşsa
                    - filtering sonrası candidate kalmamışsa

        Design Note:
            Bu service selection logic'i yönetir ancak skor üretmez.

            Skor üretimi:
                ScoringEngine sorumluluğudur.

            Böylece:
                - ranking algoritması bağımsız gelişebilir
                - selection orchestration sade kalır
                - farklı scoring stratejileri kolayca denenebilir

        Example:
            selected_question = service.select_question(
                questions=question_bank,
                context=context,
            )

            print(selected_question.text)
        """

        # ---------------------------------------------------------
        # QUESTION FILTERING
        # ---------------------------------------------------------
        # Daha önce sorulmuş sorular candidate pool'dan çıkarılır.
        #
        # Neden?
        #   Aynı sorunun tekrar tekrar sorulması:
        #       - interview kalitesini düşürür
        #       - diversity'yi azaltır
        #       - gerçek skill coverage'i engeller
        #
        # asked_question_ids:
        #   interview memory/state üzerinden gelir.
        #
        # Bu yaklaşım interview progression'ın doğal ilerlemesini sağlar.
        available_questions = [
            question
            for question in questions
            if question.id not in context.asked_question_ids
        ]

        # ---------------------------------------------------------
        # EMPTY POOL CHECK
        # ---------------------------------------------------------
        # Filtreleme sonrası candidate soru kalmamış olabilir.
        #
        # Örnek senaryolar:
        #   - tüm soru bankası tüketilmiş olabilir
        #   - input listesi zaten boş olabilir
        #   - aggressive filtering uygulanmış olabilir
        #
        # Bu durumda selection yapılamaz.
        if not available_questions:
            raise ValueError("No available questions to select.")

        # ---------------------------------------------------------
        # BEST QUESTION SELECTION
        # ---------------------------------------------------------
        # Her soru scoring engine üzerinden skorlanır.
        #
        # max(..., key=...)
        # kullanarak en yüksek skorlu soru seçilir.
        #
        # Bu yapı sayesinde:
        #   - selection orchestration burada kalır
        #   - ranking logic scoring engine içinde izole edilir
        #
        # Scoring engine şunları dikkate alabilir:
        #   - level compatibility
        #   - CV gap
        #   - market weight
        #   - category diversity
        #   - recent performance
        #   - semantic diversity
        #
        # Bu service bunların detayını bilmez.
        return max(
            available_questions,
            key=lambda question: self.scoring_engine.score(
                question,
                context,
            ),
        )
