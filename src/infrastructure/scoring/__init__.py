from abc import ABC, abstractmethod

from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext


class ScoringEngine(ABC):
    """
    Interview question selection sürecinde kullanılacak scoring strategy
    contract'ını tanımlayan abstract base interface.

    Bu interface'in temel amacı, bir Question nesnesinin mevcut interview
    context içinde ne kadar uygun olduğunu sayısal olarak değerlendiren
    algoritmaları soyutlamaktır.

    Temel fikir:
        Question selection işlemi iki ayrı responsibility'e ayrılmıştır:

            1. Selection orchestration
            2. Scoring strategy

    Bu interface ikinci kısmı temsil eder:
        yani "bir soru ne kadar uygun?" sorusunun cevabını üretir.

    Neden ayrı bir scoring abstraction gerekli?
        Çünkü interview sistemlerinde soru seçme mantığı zamanla ciddi şekilde
        karmaşıklaşabilir.

        Örneğin scoring şunlara göre değişebilir:
            - candidate seviyesi
            - CV skill gap
            - market trendleri
            - geçmiş interview performansı
            - fatigue seviyesi
            - soru çeşitliliği
            - semantic similarity
            - adaptive learning sinyalleri
            - reinforcement feedback
            - hiring policy değişiklikleri

        Eğer tüm bu logic doğrudan QuestionSelectionService içine yazılırsa:
            - servis şişer
            - SRP bozulur
            - test yazımı zorlaşır
            - yeni scoring algoritması eklemek riskli hale gelir

    Bu yüzden scoring logic soyutlanmıştır.

    Mimari ayrım:
        QuestionSelectionService:
            selection orchestration yönetir

        ScoringEngine:
            suitability scoring üretir

    Bu ayrım neden önemli?
        Çünkü:
            selection flow ile scoring algoritması farklı sorumluluklardır.

    Örnek:
        SelectionService şunları yapabilir:
            - already asked question filtreleme
            - category diversity kontrolü
            - fatigue filtering
            - candidate state yönetimi
            - en yüksek skorlu soruyu seçme

        ScoringEngine ise yalnızca:
            "Bu soru ne kadar uygun?"
        sorusuna cevap verir.

    Bu interface ne yapmaz?
        - soru seçmez
        - question list filtrelemez
        - ranking orchestration yapmaz
        - interview state mutate etmez
        - explanation üretmez
        - persistence işlemi yapmaz
        - retrieval çalıştırmaz

    Bu interface neyi garanti eder?
        Her scoring implementasyonu:

            Question + ScoringContext
                ↓
            numeric suitability score

        üretmek zorundadır.

    Bu yapı hangi SOLID prensiplerine uygundur?

        Dependency Inversion Principle:
            Selection service concrete scoring implementation'a değil,
            abstraction'a bağımlıdır.

        Open/Closed Principle:
            Yeni scoring algoritmaları mevcut sistemi değiştirmeden
            eklenebilir.

    Örnek implementasyonlar:
        - WeightedScoringEngine
        - RuleBasedScoringEngine
        - AdaptiveScoringEngine
        - MLScoringEngine
        - SemanticSimilarityScoringEngine
        - HybridScoringEngine
        - RandomScoringEngine (test/demo)

    Örnek kullanım:
        scoring_engine.score(
            question=question,
            context=context,
        )

    Önemli:
        Bu interface deterministic scoring davranışını teşvik eder.

        Yani aynı:
            - question
            - context
        için mümkün olduğunca aynı skorun üretilmesi beklenir.

        Bu:
            - debugging
            - analytics
            - reproducibility
            - testability
        açısından önemlidir.
    """

    @abstractmethod
    def score(
        self,
        question: Question,
        context: ScoringContext,
    ) -> float:
        """
        Verilen Question nesnesinin mevcut interview context içinde
        ne kadar uygun olduğunu temsil eden numeric suitability score üretir.

        Bu metod scoring engine'in temel capability contract'ıdır.

        Scoring semantics:
            Daha yüksek skor:
                sorunun mevcut context için daha uygun olduğunu

            Daha düşük skor:
                sorunun daha az uygun olduğunu

            ifade eder.

        Örnek:
            9.2
                → çok uygun soru

            4.5
                → orta uygunluk

            0.8
                → düşük uygunluk

        Bu skor nasıl kullanılabilir?
            QuestionSelectionService tipik olarak:
                - candidate question'ları iterate eder
                - her soru için score üretir
                - en yüksek skorlu soruyu seçer

        Örnek akış:
            questions
                ↓
            scoring_engine.score(...)
                ↓
            ranking
                ↓
            highest score selection

        Scoring sırasında kullanılabilecek sinyaller:
            - level compatibility
            - difficulty matching
            - CV skill gap
            - market weight
            - fatigue state
            - category diversity
            - recent performance
            - semantic novelty
            - question repetition penalty
            - adaptive pacing

        Context neden gerekli?
            Çünkü bir sorunun uygunluğu yalnızca sorunun kendisine bağlı değildir.

            Aynı soru:
                - farklı candidate level
                - farklı geçmiş performans
                - farklı fatigue state
                - farklı interview stage
            için farklı skor alabilir.

        Örnek:
            Senior-level system design sorusu:

                JR candidate için:
                    düşük skor

                SENIOR candidate için:
                    yüksek skor

        Bu yüzden scoring context-aware çalışır.

        Args:
            question:
                Skorlanacak Question entity nesnesi.

            context:
                Mevcut interview state'ini temsil eden scoring context.

                İçerebilir:
                    - current_level
                    - recent_scores
                    - asked_questions
                    - weak_areas
                    - cv_skills
                    - fatigue state
                    - interview progression

        Returns:
            float:
                Question suitability score.

                Daha yüksek skor:
                    daha uygun soru

                Daha düşük skor:
                    daha az uygun soru

        Raises:
            NotImplementedError:
                Abstract interface doğrudan kullanılırsa fırlatılır.

        Önemli:
            Bu metod:
                - side-effect üretmemelidir
                - context mutate etmemelidir
                - deterministic davranmalıdır
            mümkün olduğunca pure-function mantığında çalışmalıdır.

        Çünkü scoring logic:
            - test edilmesi kolay
            - analiz edilebilir
            - reproducible
        olmalıdır.
        """
        raise NotImplementedError