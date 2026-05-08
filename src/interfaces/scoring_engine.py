from abc import ABC, abstractmethod

from src.domain.question.question import Question
from src.domain.scoring.scoring_context import ScoringContext


class ScoringEngine(ABC):
    """
    Question selection sırasında kullanılacak scoring engine contract'ı.

    Bu sınıf doğrudan skor hesaplayan somut bir engine değildir.
    Bunun yerine farklı question selection stratejileri için ortak bir
    interface / contract tanımlar.

    Amaç:
        Interview sırasında hangi sorunun sorulacağını belirlerken kullanılan
        skor üretme davranışını soyutlamaktır.

    Bu abstraction sayesinde sistemde farklı scoring stratejileri
    tak-çıkar şekilde kullanılabilir.

    Örnek scoring engine implementasyonları:
        - WeightedScoringEngine:
            Market weight, CV gap, level uyumu, difficulty ve coverage gibi
            sinyalleri ağırlıklı olarak birleştirir.

        - RuleBasedScoringEngine:
            Daha basit if/else kurallarıyla seçim skoru üretir.

        - RandomScoringEngine:
            Test veya baseline karşılaştırmaları için rastgele skor döndürür.

        - ConfidenceAwareScoringEngine:
            Adayın önceki cevaplarındaki güven/skor durumuna göre soru
            zorluğunu ayarlar.

        - ExplorationExploitationScoringEngine:
            Bazen güçlü alanları derinleştirir, bazen zayıf veya eksik
            alanları keşfeder.

    Neden interface kullanıyoruz?
        - QuestionSelectionService somut scoring algoritmasına bağımlı olmaz.
        - Dependency Inversion Principle uygulanır.
        - Yeni scoring stratejileri mevcut servisleri bozmadan eklenebilir.
        - Testlerde deterministic fake scoring engine kullanılabilir.
        - Üretim ortamında daha gelişmiş multi-objective ranking yapılabilir.
        - Deneysel scoring algoritmaları kolayca A/B test edilebilir.

    Mimari konum:
        Service layer:
            QuestionSelectionService

        Interface:
            ScoringEngine

        Concrete implementations:
            WeightedScoringEngine
            RuleBasedScoringEngine
            MockScoringEngine
            MultiObjectiveScoringEngine

    Önemli tasarım notu:
        Bu interface sadece "skor üretme contract"ını tanımlar.

        Burada:
            - soru listesinden seçim yapmak
            - soruları filtrelemek
            - asked question kontrolü yapmak
            - semantic similarity elemesi yapmak
            - final question objesini döndürmek

        gibi işler yapılmamalıdır.

        Bu sorumluluklar QuestionSelectionService veya ilgili selection
        pipeline bileşenlerinde tutulmalıdır.

    Beklenen davranış:
        score(...) metodu tek bir Question ve mevcut ScoringContext için
        sayısal bir skor üretir.

        Daha yüksek skor, o sorunun mevcut interview context'i için daha
        uygun olduğunu ifade eder.

    Örnek:
        question = Question(...)
        context = ScoringContext(...)

        score = scoring_engine.score(question, context)

        if score yüksekse:
            Bu soru seçilmeye daha güçlü adaydır.

    Not:
        Bu interface bilinçli olarak float döndürür.
        Çünkü seçim mekanizması skorları karşılaştırarak en uygun soruyu
        seçebilir.

        İlerleyen fazlarda sadece float yerine SelectionExplanation veya
        ScoringResult gibi daha açıklanabilir bir response model'e geçilebilir.
    """

    @abstractmethod
    def score(
        self,
        question: Question,
        context: ScoringContext,
    ) -> float:
        """
        Verilen question + context için seçim skoru üretir.

        Bu method, bütün scoring engine implementasyonlarının uyması gereken
        ortak contract'tır.

        Her somut scoring engine bu metodu kendi seçim stratejisine göre
        implemente eder.

        Args:
            question:
                Skorlanacak Question domain modelidir.

                Bu model genellikle şu bilgileri içerir:
                    - id
                    - text
                    - category
                    - level
                    - difficulty
                    - question_type
                    - expected_points
                    - keywords
                    - market_weight

                Scoring engine bu alanları kullanarak sorunun mevcut mülakat
                için ne kadar uygun olduğunu hesaplar.

            context:
                Mevcut interview durumunu temsil eden ScoringContext modelidir.

                Bu model genellikle şu bilgileri içerir:
                    - current_level
                    - cv_skills
                    - asked_questions
                    - recent_scores
                    - weak_areas
                    - coverage bilgileri
                    - interview memory sinyalleri

                Scoring engine, soruyu sadece kendi özelliklerine göre değil,
                mevcut aday ve mülakat bağlamına göre değerlendirir.

        Returns:
            float:
                Sorunun mevcut context için seçim skorudur.

                Genel yorum:
                    - Daha yüksek skor = daha uygun soru
                    - Daha düşük skor = daha az uygun soru
                    - Negatif skor = güçlü şekilde tercih edilmemeli
                    - 0 skoru = nötr veya düşük öncelikli

                Örnek:
                    0.85 -> güçlü aday soru
                    0.40 -> orta uygunluk
                    0.05 -> düşük uygunluk
                    -1.0 -> seçilmemesi gereken soru

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan ScoringEngine
                üzerinden çağrılamaz. Mutlaka somut bir subclass tarafından
                implemente edilmelidir.

            ValueError:
                Somut implementasyonlar geçersiz question veya context
                durumlarında ValueError fırlatabilir.

        Design Note:
            Bu interface'in görevi sadece skor hesaplama davranışını
            standartlaştırmaktır.

            Final seçim algoritması burada olmamalıdır.

            Doğru ayrım şu şekildedir:

                ScoringEngine:
                    Tek bir soru için skor üretir.

                QuestionSelectionService:
                    Aday soru listesini gezer.
                    Her soru için ScoringEngine.score(...) çağırır.
                    En yüksek skorlu soruyu seçer.
                    Gerekirse selection explanation üretir.

            Bu ayrım sayesinde scoring algoritması değişse bile
            selection flow stabil kalır.
        """
        pass
