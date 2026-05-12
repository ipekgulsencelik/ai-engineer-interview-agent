class FatigueMultiplierPolicy:
    """
    Candidate fatigue sinyallerinden pacing multiplier üreten policy sınıfıdır.

    Bu policy'nin temel amacı, interview sırasında oluşan cognitive fatigue
    seviyesini sayısal bir pacing multiplier'a dönüştürmektir.

    Temel fikir:
        Interview sırasında candidate:
            - üst üste zor sorular
            - sürekli aynı category
            - sürekli aynı question type
            - yoğun system design soruları

        nedeniyle mental fatigue yaşayabilir.

    Bu fatigue durumu doğrudan:
        - question selection
        - difficulty pacing
        - adaptive scoring
        - overload prevention

    davranışlarını etkileyebilir.

    Fatigue neden multiplier'a dönüştürülüyor?
        Çünkü scoring engine'ler çoğu zaman:
            numeric adjustment signal

        ile daha kolay çalışır.

    Örnek:
        final_score =
            base_score * fatigue_multiplier

    Böylece:
        yüksek fatigue:
            skorları düşürebilir

        düşük fatigue:
            normal pacing sağlayabilir

    Bu sınıf neden gerekli?
        Eğer fatigue multiplier hesaplama logic'i doğrudan:
            QuestionFatigueService

        içine yazılırsa:

            - service şişer
            - threshold logic dağılır
            - multiplier strategy değiştirmek zorlaşır
            - test izolasyonu azalır
            - SRP bozulur

    Bu yüzden multiplier computation:
        ayrı bir policy sınıfına taşınmıştır.

    Responsibility ayrımı:
        QuestionFatigueService:
            fatigue snapshot üretir

        FatigueMultiplierPolicy:
            fatigue -> multiplier dönüşümü yapar

    Bu ayrım neden önemli?
        Çünkü:
            fatigue state computation
                ile
            pacing strategy

        farklı sorumluluklardır.

    Policy pattern avantajları:
        Bu yapı sayesinde:
            - threshold değerleri merkezi olur
            - multiplier stratejisi kolay değişir
            - A/B testing kolaylaşır
            - farklı pacing policy'leri yazılabilir
            - adaptive tuning kolaylaşır

    Örnek alternatif policy'ler:
        - LinearFatiguePolicy
        - ExponentialFatiguePolicy
        - AdaptiveFatiguePolicy
        - MLBasedFatiguePolicy

    Bu sınıf ne yapar?
        - fatigue signal'lerini toplar
        - fatigue severity belirler
        - pacing multiplier üretir

    Bu sınıf ne yapmaz?
        - fatigue snapshot üretmez
        - scoring yapmaz
        - question seçmez
        - interview state mutate etmez
        - adaptive pacing orchestration yapmaz

    Threshold yaklaşımı:
        Bu implementation threshold-based çalışır.

        Yani toplam fatigue point'e göre:
            - low fatigue
            - medium fatigue
            - high fatigue

        seviyeleri belirlenir.

    Bu yaklaşım neden tercih edildi?
        Çünkü:
            - sade
            - deterministic
            - explainable
            - test edilebilir
            - production-friendly

        bir yapıdır.

    İleride geliştirilebilir:
        - weighted fatigue scoring
        - nonlinear decay
        - candidate-specific adaptation
        - historical calibration
        - reinforcement tuning

    gibi mekanizmalar eklenebilir.
    """

    HIGH_FATIGUE_THRESHOLD = 6
    """
    High fatigue durumuna geçiş için gereken minimum fatigue point değeri.

    Eğer toplam fatigue point:
        >= 6

    ise candidate yüksek fatigue durumunda kabul edilir.

    Bu durumda:
        agresif pacing reduction uygulanır.

    Bu threshold neden önemli?
        Çünkü interview pacing davranışını doğrudan etkiler.
    """

    MEDIUM_FATIGUE_THRESHOLD = 3
    """
    Medium fatigue durumuna geçiş için gereken minimum fatigue point değeri.

    Eğer toplam fatigue point:
        >= 3

    ise candidate orta seviyede fatigue yaşamaya başlamış kabul edilir.

    Bu durumda:
        hafif pacing reduction uygulanır.
    """

    HIGH_FATIGUE_MULTIPLIER = 0.70
    """
    High fatigue durumunda uygulanacak pacing multiplier değeri.

    Semantics:
        0.70:
            scoring ve pacing davranışının ciddi şekilde yavaşlatılması

    Bu multiplier neyi etkileyebilir?
        - zor soruların skorunu düşürme
        - system design penalty
        - easier question boost
        - pacing slowdown

    Örnek:
        final_score =
            base_score * 0.70
    """

    MEDIUM_FATIGUE_MULTIPLIER = 0.85
    """
    Medium fatigue durumunda uygulanacak pacing multiplier değeri.

    Semantics:
        0.85:
            hafif pacing reduction

    Candidate tamamen overload değildir,
    ancak pacing biraz yavaşlatılabilir.
    """

    NO_FATIGUE_MULTIPLIER = 1.0
    """
    Fatigue olmadığı durumda kullanılacak normal pacing multiplier değeri.

    Semantics:
        1.0:
            scoring davranışında değişiklik yok

    Candidate normal interview pacing durumundadır.
    """

    def compute(
        self,
        *,
        high_difficulty_count: int,
        repeated_question_type_count: int,
        repeated_category_count: int,
        system_design_count: int,
    ) -> float:
        """
        Fatigue sinyallerinden pacing multiplier üretir.

        Bu metod farklı fatigue sinyallerini birleştirerek candidate'ın
        mevcut cognitive load seviyesini tahmin etmeye çalışır.

        Kullanılan sinyaller:
            - high_difficulty_count
            - repeated_question_type_count
            - repeated_category_count
            - system_design_count

        Bu sinyaller neden seçildi?
            Çünkü interview fatigue çoğu zaman:
                - difficulty overload
                - repetition
                - cognitive monotony
                - architecture-heavy questioning

            nedeniyle oluşur.

        Fatigue point nasıl hesaplanıyor?
            Şu anki implementation tüm sinyalleri eşit ağırlıklı toplar:

                fatigue_points =
                    high_difficulty_count
                    + repeated_question_type_count
                    + repeated_category_count
                    + system_design_count

        Bu yaklaşım neden tercih edildi?
            Çünkü:
                - sade
                - deterministic
                - explainable
                - debug-friendly

            bir modeldir.

        İleride geliştirilebilir:
            Örneğin system design daha ağır weighted olabilir:

                fatigue_points =
                    high_difficulty_count * 1.0
                    + repeated_category_count * 0.5
                    + system_design_count * 2.0

        Threshold davranışı:
            fatigue_points >= HIGH_FATIGUE_THRESHOLD
                → HIGH_FATIGUE_MULTIPLIER

            fatigue_points >= MEDIUM_FATIGUE_THRESHOLD
                → MEDIUM_FATIGUE_MULTIPLIER

            aksi halde
                → NO_FATIGUE_MULTIPLIER

        Bu multiplier nasıl kullanılabilir?
            Scoring engine içinde:

                final_score =
                    base_score * fatigue_multiplier

        veya:

                if multiplier < 0.8:
                    reduce_system_design_questions()

        gibi kullanılabilir.

        Args:
            high_difficulty_count:
                Son window içinde sorulan yüksek difficulty soru sayısı.

            repeated_question_type_count:
                Aynı question type tekrar sayısı.

            repeated_category_count:
                Aynı category tekrar sayısı.

            system_design_count:
                Son window içindeki system design soru sayısı.

        Returns:
            float:
                Candidate fatigue seviyesine göre pacing multiplier değeri.

                1.0:
                    normal pacing

                0.85:
                    medium fatigue

                0.70:
                    high fatigue
        """

        fatigue_points = (
            high_difficulty_count
            + repeated_question_type_count
            + repeated_category_count
            + system_design_count
        )

        if fatigue_points >= self.HIGH_FATIGUE_THRESHOLD:
            return self.HIGH_FATIGUE_MULTIPLIER

        if fatigue_points >= self.MEDIUM_FATIGUE_THRESHOLD:
            return self.MEDIUM_FATIGUE_MULTIPLIER

        return self.NO_FATIGUE_MULTIPLIER