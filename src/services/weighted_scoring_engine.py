from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext
from src.domain.scoring.semantic_diversity import (
    compute_semantic_diversity_score,
)
from src.interfaces.scoring_engine import ScoringEngine


class WeightedScoringEngine(ScoringEngine):
    """
    Faz-1 için kullanılan temel weighted scoring engine.

    Bu engine'in amacı:
        Candidate question'lar arasında mevcut interview context'i için
        en uygun soruyu sayısal olarak sıralamaktır.

    Sistem neden scoring kullanıyor?
        Çünkü question selection tamamen rastgele yapılmamalıdır.

        İyi bir interview sistemi:
            - aday seviyesine uygun
            - piyasada önemli
            - coverage açısından değerli
            - interview flow'una uyumlu

        soruları önceliklendirmelidir.

    Bu engine Faz-1 kapsamında intentionally sade tutulmuştur.

    Kullanılan scoring sinyalleri:
        1. level uyumu
        2. market weight

    Faz-1 yaklaşımı:
        Basit weighted linear combination kullanılır.

        final_score =
            level_score * 0.7
            +
            market_score * 0.3

    Neden weighted scoring?
        Çünkü her sinyalin etkisi eşit değildir.

        Örneğin:
            - aday seviyesine uygunluk çok kritiktir
            - market relevance önemli ama ikinci plandadır

        Bu yüzden:
            level_score → %70 ağırlık
            market_score → %30 ağırlık

    Mimari yaklaşım:
        Bu sınıf yalnızca ranking/scoring üretir.

        Şunları yapmaz:
            ✘ question filtering
            ✘ evaluator çağrısı
            ✘ question selection
            ✘ persistence
            ✘ retrieval orchestration

        Böylece Single Responsibility Principle korunur.

    Mimari konum:
        QuestionSelectionService
                ↓
        WeightedScoringEngine
                ↓
        score(question, context)

    Neden interface üzerinden çalışıyor?
        Çünkü QuestionSelectionService doğrudan bu implementasyona
        bağımlı olmamalıdır.

        Böylece:
            - farklı scoring engine'ler takılabilir
            - A/B test yapılabilir
            - testlerde fake engine kullanılabilir
            - algoritma bağımsız gelişebilir

    LEVEL_SCORES:
        Question level ile candidate level arasındaki uyum skorlarını tanımlar.

        Temel fikir:
            - aynı level → yüksek skor
            - yakın level → orta skor
            - çok uzak level → düşük skor

    Örnek:
        Candidate:
            MID

        Question:
            MID     → 1.0
            JR      → 0.6
            SENIOR  → 0.6

    Bu yapı:
        - interview adaptivity sağlar
        - aşırı zor/kolay soru riskini azaltır
        - doğal progression üretir

    Faz-2/Faz-3'te eklenebilecek sinyaller:
        - semantic diversity
        - category coverage
        - weak area boost
        - fatigue prevention
        - difficulty adaptation
        - recency penalty
        - confidence estimation
        - retrieval relevance
        - interview pacing

    Önemli tasarım notu:
        Bu engine deterministic çalışır.

        Aynı:
            question + context

        kombinasyonu her zaman aynı skoru üretir.

        Bu:
            - test güvenilirliği
            - debugging kolaylığı
            - reproducibility

        açısından önemlidir.
    """

    # ---------------------------------------------------------
    # LEVEL COMPATIBILITY MATRIX
    # ---------------------------------------------------------
    # Question level ile candidate current level arasındaki uyumu temsil eder.
    #
    # Yapı:
    #   (question_level, current_level) -> compatibility score
    #
    # Aynı level:
    #   1.0 → ideal eşleşme
    #
    # Yakın level:
    #   0.6 → kabul edilebilir challenge
    #
    # Çok uzak level:
    #   0.2 → düşük uygunluk
    #
    # Örnek:
    #   MID candidate için SENIOR soru:
    #       orta-zor challenge → 0.6
    #
    #   JR candidate için SENIOR soru:
    #       aşırı zor → 0.2
    #
    # Bu yapı adaptive interview davranışı sağlar.
    LEVEL_SCORES = {
        ("JR", "JR"): 1.0,
        ("MID", "MID"): 1.0,
        ("SENIOR", "SENIOR"): 1.0,
        ("JR", "MID"): 0.6,
        ("MID", "JR"): 0.6,
        ("MID", "SENIOR"): 0.6,
        ("SENIOR", "MID"): 0.6,
        ("JR", "SENIOR"): 0.2,
        ("SENIOR", "JR"): 0.2,
    }

    def score(
        self,
        question: Question,
        context: ScoringContext,
    ) -> float:
        """
        Verilen question için weighted selection skoru hesaplar.

        Bu method mevcut interview context'i dikkate alarak sorunun
        ne kadar uygun olduğunu sayısal olarak ifade eder.

        Kullanılan scoring sinyalleri:
            1. level compatibility
            2. market relevance

        Scoring akışı:
            1. level uyumu hesaplanır
            2. market weight alınır
            3. weighted combination uygulanır
            4. final skor döndürülür

        Args:
            question:
                Skorlanacak Question domain modelidir.

                Özellikle şu alanlar kullanılır:
                    - question.level
                    - question.market_weight

            context:
                Mevcut interview durumunu temsil eden context modelidir.

                Özellikle:
                    - context.current_level

                bilgisi scoring sırasında kullanılır.

        Returns:
            float:
                Sorunun mevcut context için uygunluk skorudur.

                Daha yüksek skor:
                    → daha uygun soru

                Daha düşük skor:
                    → daha düşük öncelik

                Örnek:
                    0.91 → güçlü aday
                    0.73 → iyi aday
                    0.31 → düşük uygunluk

        Design Note:
            Bu engine deterministic linear scoring kullanır.

            Avantajları:
                ✔ Basit
                ✔ Açıklanabilir
                ✔ Debug edilmesi kolay
                ✔ Test edilebilir
                ✔ Tahmin edilebilir

            Dezavantajları:
                ✘ Complex interaction modeling yok
                ✘ Long-term interview memory kullanmıyor
                ✘ Semantic diversity bilmiyor

            Bu tradeoff Faz-1 için bilinçli olarak kabul edilmiştir.

        Example:
            score = engine.score(
                question=question,
                context=context,
            )

            print(score)
        """

        # ---------------------------------------------------------
        # LEVEL COMPATIBILITY SCORE
        # ---------------------------------------------------------
        # Question level ile candidate current level arasındaki uyum hesaplanır.
        #
        # Örnek:
        #   MID candidate + MID question:
        #       1.0 → perfect match
        #
        #   MID candidate + JR question:
        #       0.6 → biraz kolay ama kabul edilebilir
        #
        #   JR candidate + SENIOR question:
        #       0.2 → çok zor
        #
        # .get(..., 0.2) fallback'i:
        #   Bilinmeyen kombinasyonlarda güvenli düşük skor sağlar.
        level_score = self.LEVEL_SCORES.get(
            (question.level, context.current_level),
            0.2,
        )

        # ---------------------------------------------------------
        # MARKET RELEVANCE SCORE
        # ---------------------------------------------------------
        # market_weight:
        #   Sorunun piyasadaki önemini temsil eder.
        #
        # Örnek:
        #   0.9 → piyasada çok kritik konu
        #   0.5 → orta önem
        #   0.1 → düşük öncelik
        #
        # Bu değer question repository veya external market analysis
        # pipeline tarafından üretilebilir.
        market_score = question.market_weight

        # ---------------------------------------------------------
        # FINAL WEIGHTED SCORE
        # ---------------------------------------------------------
        # Weighted linear combination uygulanır.
        #
        # Ağırlıklar:
        #   level_score  -> %70
        #   market_score -> %30
        #
        # Neden level daha ağır?
        #   Çünkü yanlış seviye seçimi interview kalitesini ciddi şekilde
        #   bozabilir.
        #
        # Market relevance önemli olsa da secondary signal olarak tutulur.
        #
        # Örnek:
        #   level_score = 1.0
        #   market_score = 0.8
        #
        #   final =
        #       1.0 * 0.7
        #       +
        #       0.8 * 0.3
        #
        #       = 0.94
        final_score = level_score * 0.7 + market_score * 0.3

        # ---------------------------------------------------------
        # SCORE NORMALIZATION
        # ---------------------------------------------------------
        # round(..., 4):
        #   Floating-point noise'u azaltır.
        #
        # Avantajları:
        #   - log/debug readability artar
        #   - test assertion'ları daha stabil olur
        #   - output daha temiz görünür
        #
        # Örnek:
        #   0.899999999 → 0.9
        return round(final_score, 4)

    def compute_semantic_score(
        self,
        max_similarity_to_asked: float | None,
    ) -> float:
        """
        Semantic diversity tabanlı scoring multiplier üretir.

        Bu method:
            Candidate question'ın daha önce sorulmuş sorularla semantic
            benzerliğini analiz ederek diversity-aware scoring üretir.

        Amaç:
            Interview sırasında semantic tekrarları azaltmak ve daha dengeli,
            çeşitli ve kaliteli bir interview akışı oluşturmaktır.

        Problem:
            Aynı kavram farklı kelimelerle tekrar tekrar sorulabilir.

        Örnek:
            "What is RAG?"
            "Explain Retrieval-Augmented Generation."

        Keyword açısından farklı görünseler bile semantic olarak neredeyse
        aynıdırlar.

        Bu method:
            embedding similarity

        bilgisini kullanarak bu tür semantic tekrarları penalize eder.

        Nasıl çalışır?
            1. Candidate question'ın geçmiş sorularla olan en yüksek semantic
            similarity değeri alınır.

            2. Bu similarity değeri:
                compute_semantic_diversity_score()

            helper function'ına gönderilir.

            3. Helper function:
                diversity multiplier

            üretir.

        Üretilen skor anlamı:
            1.0:
                semantic olarak yeterince farklı

            0.85:
                orta düzey semantic tekrar riski

            0.60:
                yüksek duplicate riski

        Args:
            max_similarity_to_asked:
                Candidate question'ın daha önce sorulmuş sorularla olan
                maksimum semantic similarity değeri.

                Beklenen aralık:
                    0.0 - 1.0

                Örnek:
                    0.92 → çok yüksek similarity
                    0.78 → orta similarity
                    0.25 → düşük similarity

                None:
                    semantic similarity bilgisi mevcut değil

        Returns:
            float:
                Semantic diversity multiplier skoru.

                Bu skor genellikle:
                    final weighted scoring

                içerisinde multiplier veya signal olarak kullanılır.

        Design Note:
            Bu method doğrudan scoring logic içermez.

            Gerçek semantic diversity hesaplaması:
                compute_semantic_diversity_score()

            helper function'ına delegasyon yapılır.

            Bunun avantajları:
                ✔ Single Responsibility Principle
                ✔ reusable scoring logic
                ✔ cleaner orchestration
                ✔ easier unit testing
                ✔ centralized semantic scoring rules

        Mimari yaklaşım:
            Bu method:
                orchestration adapter

            gibi davranır.

            Semantic scoring algoritmasının detaylarını bilmez.
            Yalnızca ilgili helper function'ı çağırır.

        Gelecekte geliştirilebilecek alanlar:
            - category-aware semantic diversity
            - recency-aware duplicate penalty
            - adaptive thresholding
            - nonlinear semantic penalty
            - embedding confidence weighting
            - semantic cluster balancing

        Example:
            score = self.compute_semantic_score(
                max_similarity_to_asked=0.91
            )

            print(score)

        Output:
            0.60
        """

        # ---------------------------------------------------------
        # SEMANTIC DIVERSITY SCORING
        # ---------------------------------------------------------
        # Semantic duplicate riskine göre diversity multiplier hesaplanır.
        #
        # Helper function:
        #   - threshold evaluation yapar
        #   - duplicate riskini analiz eder
        #   - uygun penalty multiplier döndürür
        return compute_semantic_diversity_score(max_similarity_to_asked)
