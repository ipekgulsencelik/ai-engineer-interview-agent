from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionFatigue:
    """
    Candidate cognitive fatigue durumunu temsil eden immutable runtime
    snapshot modelidir.

    Bu model interview sırasında adayın bilişsel yük seviyesini temsil eden
    sinyalleri taşır.

    Temel amaç:
        Interview sisteminin adaya:
            - üst üste çok zor
            - üst üste aynı tipte
            - üst üste aynı kategoride
            - sürekli system design ağırlıklı

        soru sormasını engellemeye yardımcı olmaktır.

    Neden fatigue tracking gerekli?
        Teknik interview süreçlerinde yalnızca:
            "en zor"
            veya
            "en alakalı"

        soruları seçmek iyi interview deneyimi üretmez.

        Çünkü candidate zamanla:
            - mental overload yaşayabilir
            - performans düşüşü gösterebilir
            - düşünme kalitesi kaybedebilir
            - communication kalitesi düşebilir

    Örnek problem:
        Üst üste:
            - distributed systems
            - system design
            - scalability
            - architecture trade-off

        soruları sorulursa candidate cognitive fatigue yaşayabilir.

        Bu durumda gerçek bilgi seviyesi doğru ölçülemeyebilir.

    QuestionFatigue modeli bu problemi azaltmak için kullanılır.

    Bu model neyi temsil eder?
        Bu model:
            "candidate overload snapshot"

        gibi düşünülebilir.

    Bu model ne yapar?
        - fatigue sinyallerini taşır
        - overload riskini temsil eder
        - scoring engine'e pacing bilgisi sağlar
        - adaptive interview davranışını destekler

    Bu model ne yapmaz?
        - fatigue hesaplamaz
        - scoring yapmaz
        - pacing strategy üretmez
        - question seçmez
        - interview state mutate etmez

    Fatigue computation neden burada değil?
        Çünkü bu model immutable snapshot temsil eder.

        Fatigue hesaplama logic'i:
            - QuestionFatigueService
            - analytics builder
            - pacing service

        gibi ayrı yapılarda bulunmalıdır.

    Bu ayrım neden önemli?
        Çünkü:
            state representation
                ile
            state computation

        farklı sorumluluklardır.

    Immutable tasarım:
        frozen=True kullanılmıştır.

        Çünkü scoring sırasında kullanılan fatigue snapshot:
            - deterministic
            - reproducible
            - side-effect free

        olmalıdır.

    Interview pacing açısından önemi:
        Bu model sayesinde sistem:
            - daha dengeli interview akışı
            - daha doğal pacing
            - daha gerçekçi assessment
            - candidate-friendly deneyim

        üretebilir.

    Örnek kullanım:
        fatigue = QuestionFatigue(
            high_difficulty_count=3,
            repeated_category_count=2,
            fatigue_multiplier=0.72,
        )

        if fatigue.is_high_fatigue():
            reduce_system_design_questions()

    Bu yaklaşım adaptive interview sistemleri için kritik öneme sahiptir.
    """

    high_difficulty_count: int = 0
    """
    Son interview penceresinde kaç adet yüksek difficulty seviyeli soru
    sorulduğunu temsil eder.

    Örnek:
        Son birkaç soru:
            - distributed systems
            - consensus algorithms
            - large-scale architecture

        gibi yüksek bilişsel yük gerektiriyorsa bu değer artabilir.

    Bu alan neden önemlidir?
        Çünkü üst üste zor soru sormak:
            - cognitive overload
            - performans düşüşü
            - düşünme kalitesinde bozulma

        oluşturabilir.

    Scoring engine bu alanı kullanarak:
        - daha hafif soru seçebilir
        - difficulty pacing uygulayabilir
        - adaptive balancing yapabilir

    Örnek:
        high_difficulty_count yüksekse:
            yeni high-difficulty sorulara penalty uygulanabilir.
    """

    repeated_question_type_count: int = 0
    """
    Aynı question type'ın art arda kaç kez tekrarlandığını temsil eder.

    Örnek:
        Üst üste:
            - conceptual
            - conceptual
            - conceptual

        soruları soruluyorsa bu değer yükselebilir.

    Bu alan neden önemlidir?
        Çünkü sürekli aynı düşünme biçimini ölçen sorular:
            - interview monotonluğu
            - candidate yorgunluğu
            - değerlendirme daralması

        yaratabilir.

    Amaç:
        Question type diversity sağlamaktır.

    Örnek:
        conceptual sonrası:
            debugging veya scenario

        sorusu seçilebilir.
    """

    repeated_category_count: int = 0
    """
    Aynı kategoriden üst üste kaç soru sorulduğunu temsil eder.

    Örnek:
        Üst üste:
            - RAG
            - RAG
            - RAG

        soruları soruluyorsa bu değer yükselebilir.

    Bu alan neden önemlidir?
        Çünkü interview coverage tek kategoriye sıkışmamalıdır.

        Aksi halde:
            - assessment daralır
            - candidate'ın genel seviyesi ölçülemez
            - interview repetitive hale gelir

    Scoring engine:
        repeated_category_count yüksek olduğunda
        farklı kategorilere boost verebilir.
    """

    system_design_count: int = 0
    """
    Son interview penceresinde kaç adet system design odaklı soru
    sorulduğunu temsil eder.

    System design soruları neden özel takip ediliyor?
        Çünkü bu soru tipi:
            - yüksek cognitive load
            - uzun reasoning
            - yoğun architecture thinking

        gerektirir.

    Üst üste çok fazla system design sorusu:
        - candidate mental fatigue
        - communication düşüşü
        - reasoning performansında azalma

        oluşturabilir.

    Bu nedenle system design soruları çoğu zaman:
        - pacing
        - balancing
        - fatigue management

    açısından özel ele alınır.
    """

    fatigue_multiplier: float = 1.0
    """
    Candidate fatigue seviyesini temsil eden normalize edilmiş pacing
    multiplier değeridir.

    Bu alan scoring engine için en önemli fatigue sinyalidir.

    Semantics:
        1.0
            → fatigue yok / normal pacing

        0.9
            → hafif fatigue

        0.7
            → yüksek fatigue

        0.5
            → ciddi overload riski

    Bu multiplier nasıl kullanılabilir?
        Scoring engine bazı soru tiplerinin skorunu azaltabilir.

    Örnek:
        final_score =
            base_score * fatigue_multiplier

    Böylece yüksek fatigue durumunda:
        - ağır sorular geri plana düşebilir
        - daha dengeli pacing sağlanabilir

    Bu alan:
        - adaptive pacing
        - overload prevention
        - interview balancing

    açısından kritik sinyaldir.
    """

    def is_high_fatigue(self) -> bool:
        """
        Candidate fatigue seviyesinin yüksek olup olmadığını döndürür.

        Bu metod scoring engine veya pacing logic tarafından hızlı decision
        helper olarak kullanılabilir.

        Threshold:
            fatigue_multiplier < 0.8

        neden seçildi?
            Çünkü:
                0.8 altı genellikle noticeable fatigue seviyesini temsil eder.

        Bu threshold ileride:
            - configuration
            - adaptive calibration
            - analytics-driven tuning

        ile değiştirilebilir.

        Returns:
            bool:
                True:
                    candidate yüksek fatigue durumunda

                False:
                    fatigue kabul edilebilir seviyede
        """
        return self.fatigue_multiplier < 0.8