from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringSignals:
    """
    Question selection sırasında kullanılan scoring sinyallerini temsil eden
    immutable domain model.

    Bu modelin amacı:
        Bir question'ın neden belirli bir skor aldığını açıklanabilir ve
        parçalanabilir şekilde temsil etmektir.

    Neden ayrı bir scoring signal modeli gerekiyor?
        Çünkü production-grade interview sistemlerinde:
            "final score"

        tek başına yeterli değildir.

        Sistem aynı zamanda şunu da açıklayabilmelidir:
            "Bu soru neden seçildi?"

    Bu model sayesinde scoring:
        ✔ explainable hale gelir
        ✔ debug edilebilir olur
        ✔ telemetry üretilebilir
        ✔ analytics desteklenir
        ✔ tuning kolaylaşır
        ✔ A/B test yapılabilir

    Örnek:
        final_score = 0.82

        Tek başına çok anlamlı değildir.

        Ancak breakdown ile:
            level_score      = 0.9
            market_score     = 0.8
            diversity_score  = -0.1
            fatigue_score    = -0.2

        şeklinde görülebilir.

    Böylece sistem:
        - neden seçim yaptığını açıklayabilir
        - hangi sinyalin baskın olduğunu gösterebilir
        - tuning sırasında hangi weight'in problem yarattığını analiz edebilir

    Bu model hangi sistemlerde kullanılabilir?
        - WeightedScoringEngine
        - analytics dashboard
        - interview telemetry
        - debugging
        - ranking visualization
        - selection explanation builder
        - evaluation observability

    Neden frozen=True?
        Çünkü scoring signals:
            belirli bir scoring anının immutable snapshot'ıdır.

        Sonradan değiştirilmeleri:
            - debugging zorluğu
            - inconsistent analytics
            - telemetry corruption
            - nondeterministic behavior

        oluşturabilir.

    Bu modelin yaklaşımı:
        Final score yerine:
            component-based scoring

        kullanmaktır.

    Bu sayede sistem:
        - modular
        - explainable
        - extensible

    hale gelir.

    Şu an desteklenen sinyaller:
        - level_score
        - market_score
        - diversity_score
        - semantic_score
        - fatigue_score

    Faz-1'de aktif kullanılanlar:
        - level_score
        - market_score

    Diğer alanlar:
        Faz-2/Faz-3 genişlemeleri için hazırlanmıştır.

    Gelecekte eklenebilecek sinyaller:
        - weak_area_score
        - recency_penalty
        - exploration_score
        - confidence_score
        - coverage_penalty
        - personalization_score
        - memory_graph_score
        - retrieval_relevance

    Önemli tasarım notu:
        Bu model scoring algoritmasını içermez.

        Sadece:
            scoring decomposition sonucu

        temsil eder.

        Yani:
            nasıl skor hesaplandığı
        değil,
            hangi skor bileşenlerinin oluştuğu

        bilgisini taşır.
    """

    # ---------------------------------------------------------
    # LEVEL COMPATIBILITY SCORE
    # ---------------------------------------------------------
    # Question level ile candidate current level arasındaki uyumu temsil eder.
    #
    # Amaç:
    #   Sorunun aday için:
    #       - çok kolay
    #       - çok zor
    #       - uygun challenge
    #
    # olup olmadığını ölçmek.
    #
    # Örnek:
    #   MID candidate + MID question:
    #       yüksek score
    #
    #   JR candidate + SENIOR question:
    #       düşük score
    #
    # Genellikle interview adaptivity'nin en güçlü sinyallerinden biridir.
    level_score: float

    # ---------------------------------------------------------
    # MARKET RELEVANCE SCORE
    # ---------------------------------------------------------
    # Sorunun güncel iş piyasasındaki önemini temsil eder.
    #
    # Amaç:
    #   Industry açısından kritik skill'leri daha sık önceliklendirmek.
    #
    # Örnek:
    #   modern RAG systems:
    #       yüksek market relevance
    #
    #   eski/deprecated teknoloji:
    #       düşük relevance
    #
    # Bu değer:
    #   - manuel expert input
    #   - job scraping
    #   - hiring analytics
    #
    # üzerinden üretilebilir.
    market_score: float

    # ---------------------------------------------------------
    # DIVERSITY SCORE
    # ---------------------------------------------------------
    # Interview diversity katkısını temsil eder.
    #
    # Amaç:
    #   Aynı category/type tekrarını azaltmak.
    #
    # Örnek:
    #   Sürekli RAG sorusu soruluyorsa:
    #       diversity penalty uygulanabilir.
    #
    # Bu sayede interview:
    #   - daha dengeli
    #   - daha kapsamlı
    #   - daha az monoton
    #
    # hale gelir.
    #
    # Faz-1'de aktif kullanılmasa da future-ready olarak eklenmiştir.
    diversity_score: float = 0.0

    # ---------------------------------------------------------
    # SEMANTIC RELEVANCE SCORE
    # ---------------------------------------------------------
    # Semantic similarity/retrieval tabanlı uygunluk skorudur.
    #
    # Amaç:
    #   Question'ın:
    #       - candidate CV'si
    #       - weak areas
    #       - retrieval query
    #       - interview memory
    #
    # ile semantic uyumunu ölçmek.
    #
    # Örnek:
    #   Candidate embedding experience içeriyorsa:
    #       embedding-related questions boost alabilir.
    #
    # Genellikle vector search / embedding retrieval sistemleriyle çalışır.
    semantic_score: float = 0.0

    # ---------------------------------------------------------
    # FATIGUE SCORE
    # ---------------------------------------------------------
    # Candidate cognitive fatigue etkisini temsil eder.
    #
    # Amaç:
    #   Üst üste:
    #       - çok zor
    #       - çok yoğun
    #       - çok benzer
    #
    # sorular sorulmasını engellemek.
    #
    # Örnek:
    #   Son 5 soru da system design ise:
    #       fatigue penalty uygulanabilir.
    #
    # Bu sayede:
    #   - interview pacing iyileşir
    #   - candidate burnout azalır
    #   - daha doğal conversation flow oluşur
    fatigue_score: float = 0.0

    def total(self) -> float:
        """
        Tüm scoring sinyallerini birleştirerek final score üretir.

        Bu method:
            scoring signal aggregation

        işlemini temsil eder.

        Şu an kullanılan yaklaşım:
            Basit additive scoring.

        Formula:
            total =
                level_score
                + market_score
                + diversity_score
                + semantic_score
                + fatigue_score

        Returns:
            float:
                Toplam birleşik skor.

                Daha yüksek skor:
                    → daha uygun question

                Daha düşük skor:
                    → daha düşük öncelik

        Design Note:
            Şu an simple additive model kullanılmaktadır.

            Avantajları:
                ✔ Basit
                ✔ Explainable
                ✔ Debuggable
                ✔ Deterministic

            Dezavantajları:
                ✘ Weight normalization yok
                ✘ Dynamic weighting yok
                ✘ Nonlinear interaction modeling yok

        Gelecekte gelişebilecek alanlar:
            - weighted aggregation
            - dynamic weights
            - nonlinear scoring
            - reinforcement-based tuning
            - probabilistic ranking
            - learned ranking models

        Example:
            signals = ScoringSignals(
                level_score=0.8,
                market_score=0.7,
                diversity_score=-0.1,
            )

            print(signals.total())

        Output:
            1.4
        """

        # ---------------------------------------------------------
        # SIGNAL AGGREGATION
        # ---------------------------------------------------------
        # Tüm scoring bileşenleri tek bir final score altında toplanır.
        #
        # Bu yapı:
        #   - explainable scoring
        #   - modular ranking
        #   - telemetry analysis
        #
        # için oldukça uygundur.
        #
        # Her signal:
        #   positive contribution
        # veya
        #   negative penalty
        #
        # olarak davranabilir.
        return (
            self.level_score
            + self.market_score
            + self.diversity_score
            + self.semantic_score
            + self.fatigue_score
        )
