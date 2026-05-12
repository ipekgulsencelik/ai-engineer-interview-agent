from src.domain.enums.level import Level
from src.domain.config.level_transition_config import (
    LevelTransitionConfig,
)
from src.domain.constants.levels import (
    LEVEL_ORDER,
)


class LevelTransitionPolicy:
    """
    Interview level transition kararını veren core business policy.

    Bu sınıfın temel amacı:
        Candidate'in recent performance trend'ini analiz ederek
        interview seviyesinin:
            - yükseltilip yükseltilmeyeceğine
            - düşürülüp düşürülmeyeceğine
            - korunup korunmayacağına
        karar vermektir.

    Bu sınıf neden önemlidir?
        Adaptive interview sistemlerinde candidate difficulty seviyesi
        dinamik şekilde yönetilmelidir.

        Çünkü:
            - çok başarılı adaylar challenge edilmelidir
            - zorlanan adaylar overload yaşamamalıdır
            - interview pacing doğal hissettirmelidir

    Bu policy tam olarak bunu yönetir.

    ---------------------------------------------------------
    ARCHITECTURAL RESPONSIBILITY
    ---------------------------------------------------------

    Bu sınıf:
        ✔ business decision verir
        ✔ level progression yönetir
        ✔ score trend analiz eder

    Bu sınıf:
        ✘ validation yapmaz
        ✘ persistence yönetmez
        ✘ evaluator çağırmaz
        ✘ scoring üretmez
        ✘ question seçmez
        ✘ telemetry/logging yönetmez

    Böylece:
        - SRP korunur
        - test edilebilirlik artar
        - business rule isolation sağlanır

    ---------------------------------------------------------
    WHY POLICY CLASS?
    ---------------------------------------------------------

    Transition logic'in service içine gömülmesi yerine ayrı policy
    sınıfına taşınması kritik architectural avantaj sağlar.

    Çünkü:
        - business rules izole edilir
        - future strategy replacement kolaylaşır
        - A/B testing yapılabilir
        - farklı transition algoritmaları eklenebilir

    Örneğin ileride:
        - Bayesian transition
        - ML-based transition
        - confidence-aware transition
        - fatigue-aware transition
        - category-specific transition
    gibi sistemler eklenebilir.

    ---------------------------------------------------------
    LEVEL ORDER
    ---------------------------------------------------------

    Sistemdeki resmi progression sırasını tanımlar.

    JR → MID → SENIOR

    Bu sıra:
        - level up/down sırasında
        - boundary kontrolünde
        - progression traversal işlemlerinde
    kullanılır.

    Neden list kullanılıyor?
        Çünkü scalable'dır.

    Örneğin:
        STAFF
        PRINCIPAL

    gibi yeni seviyeler kolayca eklenebilir.
    """


    def __init__(
        self,
        config: LevelTransitionConfig | None = None,
    ) -> None:
        """
        LevelTransitionPolicy nesnesini başlatır.

        Args:
            config:
                Transition davranışını yöneten configuration nesnesi.

                Eğer verilmezse default configuration kullanılır.

        Neden dependency injection?
            Çünkü:
                - testability artar
                - farklı config profilleri kullanılabilir
                - production/dev davranışı ayrıştırılabilir
                - magic number bağımlılığı azalır
        """

        self.config = config or LevelTransitionConfig()

    def decide(
        self,
        *,
        current_level: Level,
        recent_scores: list[float],
    ) -> Level:
        """
        Recent performance trend'ine göre yeni level kararını verir.

        İşleyiş:
            1. Recent score window seçilir
            2. Average score hesaplanır
            3. Upgrade condition kontrol edilir
            4. Downgrade condition kontrol edilir
            5. Hiçbiri oluşmazsa mevcut level korunur

        Args:
            current_level:
                Candidate'in mevcut interview seviyesi.

            recent_scores:
                Candidate'in yakın geçmiş performance skorları.

        Returns:
            Level:
                Yeni transition sonucu oluşan level.

        Design Note:
            Bu method deterministic davranır.

            Aynı input:
                → her zaman aynı output'u üretir.

            Bu özellik:
                - replayability
                - testability
                - predictability
            açısından kritiktir.

        Example:
            policy.decide(
                current_level=Level.JR,
                recent_scores=[8, 9, 9],
            )

            -> Level.MID
        """

        # ---------------------------------------------------------
        # EMPTY SCORE GUARD
        # ---------------------------------------------------------
        # Henüz yeterli performance datası yoksa
        # en güvenli davranış mevcut level'i korumaktır.
        #
        # Bu durum genellikle:
        #   - interview başlangıcında
        #   - evaluation failure senaryolarında
        # ortaya çıkar.
        if not recent_scores:
            return current_level

        # ---------------------------------------------------------
        # RECENT WINDOW SELECTION
        # ---------------------------------------------------------
        # Sadece son N skor dikkate alınır.
        #
        # Neden tüm geçmiş kullanılmıyor?
        #
        # Çünkü:
        #   sistem candidate'in güncel performansına
        #   daha duyarlı olmalıdır.
        #
        # Eski performans:
        #   sonsuza kadar sistemi etkilememelidir.
        recent_window = recent_scores[
            -self.config.recent_window_size :
        ]

        # ---------------------------------------------------------
        # AVERAGE PERFORMANCE
        # ---------------------------------------------------------
        # Recent score ortalaması hesaplanır.
        #
        # Bu ortalama:
        #   transition kararının ana sinyalidir.
        average_score = self._compute_average(
            recent_window,
        )

        # ---------------------------------------------------------
        # CURRENT POSITION
        # ---------------------------------------------------------
        # Mevcut level progression index'i bulunur.
        #
        # Örnek:
        #   JR      -> 0
        #   MID     -> 1
        #   SENIOR  -> 2
        current_index = LEVEL_ORDER.index(
            current_level,
        )

        # ---------------------------------------------------------
        # UPGRADE DECISION
        # ---------------------------------------------------------
        # Candidate mevcut seviyeyi rahat yönetiyorsa
        # bir üst seviyeye geçirilir.
        #
        # Boundary protection:
        #   En üst level daha yukarı çıkamaz.
        if self._should_upgrade(
            average_score=average_score,
            current_index=current_index,
        ):
            return LEVEL_ORDER[current_index + 1]

        # ---------------------------------------------------------
        # DOWNGRADE DECISION
        # ---------------------------------------------------------
        # Candidate mevcut seviyede ciddi zorlanıyorsa
        # daha düşük seviyeye geçirilir.
        #
        # Amaç:
        #   cognitive overload önlemek.
        #
        # Boundary protection:
        #   En düşük level daha aşağı inemez.
        if self._should_downgrade(
            average_score=average_score,
            current_index=current_index,
        ):
            return self.LEVEL_ORDER[current_index - 1]

        # ---------------------------------------------------------
        # STABLE LEVEL
        # ---------------------------------------------------------
        # Candidate ne çok zorlanıyor ne de tamamen domine ediyor.
        #
        # Bu durumda mevcut level korunur.
        return current_level

    @staticmethod
    def _compute_average(
        scores: list[float],
    ) -> float:
        """
        Score ortalamasını hesaplar.

        Bu method:
            recent performance trend'ini
            numerically summarize eder.

        Args:
            scores:
                Average alınacak score listesi.

        Returns:
            float:
                Arithmetic mean değeri.

        Example:
            [8, 9, 7]
                -> 8.0

        Neden average kullanılıyor?
            Çünkü:
                - noise reduction sağlar
                - tekil outlier etkisini azaltır
                - daha stabil transition behavior üretir
        """

        return sum(scores) / len(scores)


    def _should_upgrade(
        self,
        *,
        average_score: float,
        current_index: int,
    ) -> bool:
        """
        Candidate'in level up olması gerekip gerekmediğini belirler.

        Upgrade condition:
            average_score >= upgrade_threshold

        Ayrıca:
            candidate zaten en üst level'da olmamalıdır.

        Args:
            average_score:
                Recent performance average değeri.

            current_index:
                Current level progression index'i.

        Returns:
            bool:
                True  -> level up gerekli
                False -> level up gerekmiyor
        """

        return (
            average_score >= self.config.upgrade_threshold
            and current_index < len(LEVEL_ORDER) - 1
        )

    def _should_downgrade(
        self,
        *,
        average_score: float,
        current_index: int,
    ) -> bool:
        """
        Candidate'in level down olması gerekip gerekmediğini belirler.

        Downgrade condition:
            average_score <= downgrade_threshold

        Ayrıca:
            candidate zaten minimum level'da olmamalıdır.

        Args:
            average_score:
                Recent performance average değeri.

            current_index:
                Current level progression index'i.

        Returns:
            bool:
                True  -> level down gerekli
                False -> level down gerekmiyor
        """

        return (
            average_score <= self.config.downgrade_threshold
            and current_index > 0
        )