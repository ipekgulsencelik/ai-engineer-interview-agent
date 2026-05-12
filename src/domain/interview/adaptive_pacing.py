from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptivePacing:
    """
    Interview pacing ve difficulty adaptation stratejisini temsil eden
    immutable runtime domain modelidir.

    Bu modelin temel amacı, candidate'ın:
        - son performansı
        - cognitive fatigue durumu
        - interview progression seviyesi

    gibi sinyallere göre interview akışının dinamik olarak ayarlanmasını
    sağlamaktır.

    Adaptive pacing neden gerekli?
        Teknik interview süreçleri statik şekilde ilerlediğinde şu problemler
        oluşabilir:

            - candidate overload
            - sürekli aşırı zor soru
            - sürekli aşırı kolay soru
            - pacing bozulması
            - yanlış seviye ölçümü
            - candidate confidence kaybı

    Örnek problem:
        Candidate son 3 soruda düşük performans gösterdiyse,
        sistem hala aynı difficulty seviyesinde devam ederse:

            - gerçek bilgi seviyesi yanlış ölçülebilir
            - candidate mental block yaşayabilir
            - interview verimsiz hale gelebilir

    AdaptivePacing bu problemi çözmeye yardımcı olur.

    Temel fikir:
        Interview sistemi candidate davranışına adapte olmalıdır.

    Örnek:
        Candidate:
            - yüksek skor alıyorsa
            - hızlı reasoning yapıyorsa
            - fatigue düşükse

        daha zor sorular seçilebilir.

        Candidate:
            - düşük skor alıyorsa
            - fatigue yüksekse
            - pacing bozuluyorsa

        daha dengeli veya daha kolay sorular seçilebilir.

    Bu model neyi temsil eder?
        Bu model:
            "mevcut pacing recommendation snapshot"

        gibi düşünülebilir.

    Bu model ne yapar?
        - adaptive pacing sinyallerini taşır
        - difficulty adaptation bilgisini sağlar
        - scoring engine'e pacing rehberliği sunar
        - runtime interview state'ini temsil eder

    Bu model ne yapmaz?
        - pacing hesaplamaz
        - difficulty seçmez
        - score üretmez
        - question seçmez
        - fatigue hesaplamaz
        - interview flow yönetmez

    Adaptive pacing computation neden burada değil?
        Çünkü bu model immutable runtime snapshot temsil eder.

        Adaptive pacing hesaplama logic'i:
            - AdaptivePacingService
            - pacing engine
            - interview analytics service

        gibi yapılarda bulunmalıdır.

    Bu ayrım neden önemli?
        Çünkü:
            pacing computation
                ile
            pacing state representation

        farklı sorumluluklardır.

    Immutable tasarım:
        frozen=True kullanılmıştır.

        Çünkü pacing snapshot:
            - deterministic
            - reproducible
            - side-effect free

        olmalıdır.

        Eğer pacing state scoring sırasında mutate edilirse:
            - selection davranışı değişebilir
            - debugging zorlaşabilir
            - analytics güvenilirliği düşebilir

    Adaptive interview açısından önemi:
        Bu model sayesinde interview sistemi:
            - daha doğal pacing
            - daha gerçekçi assessment
            - candidate-friendly deneyim
            - daha dengeli difficulty progression

        sağlayabilir.

    Örnek kullanım:
        pacing = AdaptivePacing(
            target_difficulty=2,
            difficulty_multiplier=0.85,
            should_reduce_difficulty=True,
        )

        scoring engine daha sonra:
            - senior design sorularını geri plana düşürebilir
            - daha orta difficulty sorulara boost verebilir

    Bu yaklaşım özellikle:
        - adaptive interview systems
        - AI interviewer
        - intelligent assessment platform

    gibi yapılarda kritik öneme sahiptir.
    """

    target_difficulty: int | None = None
    """
    Interview'in yönelmesi önerilen hedef difficulty seviyesini temsil eder.

    Örnek:
        1:
            daha temel / kolay sorular

        2:
            orta seviye sorular

        3:
            daha zor / advanced sorular

    Bu alan neden önemlidir?
        Çünkü adaptive pacing sistemi candidate'ın mevcut durumuna göre
        interview difficulty seviyesini yönlendirebilir.

    Örnek:
        Candidate son sorularda zorlanıyorsa:
            target_difficulty=1 veya 2 olabilir.

        Candidate çok güçlü performans gösteriyorsa:
            target_difficulty=3 olabilir.

    Bu alan scoring engine tarafından:
        - difficulty matching
        - adaptive filtering
        - pacing-aware scoring

    için kullanılabilir.

    None ne anlama gelir?
        Sistem şu anda belirli bir difficulty hedefi önermiyor demektir.

        Bu durumda scoring engine normal davranışına devam edebilir.
    """

    difficulty_multiplier: float = 1.0
    """
    Difficulty bazlı scoring adjustment multiplier değeridir.

    Bu multiplier scoring engine tarafından:
        - zor soruların boost/penalty alması
        - kolay soruların öne çıkarılması
        - pacing dengesinin sağlanması

    için kullanılabilir.

    Semantics:
        1.0
            → normal pacing

        0.8
            → difficulty azaltma eğilimi

        1.2
            → difficulty artırma eğilimi

    Örnek:
        final_score =
            base_score * difficulty_multiplier

    Candidate fatigue yüksekse:
        multiplier düşürülebilir.

    Candidate çok güçlü performans gösteriyorsa:
        multiplier artırılabilir.

    Bu alan:
        - adaptive scoring
        - pacing control
        - overload prevention
        - progression tuning

    açısından önemlidir.
    """

    should_reduce_difficulty: bool = False
    """
    Interview difficulty seviyesinin azaltılması gerektiğini belirten sinyaldir.

    Bu flag neden gerekli?
        Çünkü bazı durumlarda sistem açık şekilde:
            "candidate overload yaşamaya başladı"

        sonucuna ulaşabilir.

    Örnek trigger durumları:
        - düşük recent_scores
        - yüksek fatigue
        - uzun response latency
        - communication düşüşü
        - reasoning quality azalması

    Bu durumda scoring engine:
        - daha kolay sorulara boost verebilir
        - ağır system design sorularını geri plana düşürebilir
        - pacing'i yavaşlatabilir

    Bu alan adaptive interview deneyimi için kritik sinyaldir.
    """

    should_increase_difficulty: bool = False
    """
    Interview difficulty seviyesinin artırılması gerektiğini belirten sinyaldir.

    Bu flag neden gerekli?
        Çünkü bazı candidate'lar mevcut interview seviyesini çok rahat
        geçebilir.

    Örnek trigger durumları:
        - sürekli yüksek skor
        - hızlı reasoning
        - güçlü teknik derinlik
        - düşük fatigue
        - yüksek confidence

    Bu durumda sistem:
        - daha zor sorular seçebilir
        - daha advanced system design soruları sorabilir
        - deeper probing yapabilir

    Amaç:
        Candidate'ın gerçek upper-bound seviyesini ölçebilmektir.

    Bu alan özellikle:
        - senior hiring
        - advanced screening
        - high-signal assessment

    süreçlerinde önemlidir.
    """