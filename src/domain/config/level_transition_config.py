from dataclasses import dataclass

WINDOW_SIZE = 3 # Son kaç skorun ortalamasına bakılacağı
UPGRADE_THRESHOLD = 8.0 
DOWNGRADE_THRESHOLD = 4.0


@dataclass(frozen=True)
class LevelTransitionConfig:
    """
    Interview level transition davranışını yöneten immutable
    configuration modelidir.

    Amaç:
        Adaptive interview flow içerisinde candidate performansına göre
        level transition kararlarının merkezi ve güvenli şekilde
        konfigüre edilmesini sağlamaktır.

    Bu configuration:
        - recent performance window boyutunu belirler
        - level up threshold'unu belirler
        - level down threshold'unu belirler

    Neden immutable?
        frozen=True sayesinde runtime sırasında config mutation
        edilmesi engellenir.

        Böylece:
            - deterministic behavior sağlanır
            - side effect riski azalır
            - thread-safe kullanım kolaylaşır
            - production ortamında yanlışlıkla config değiştirilmesi
              önlenir

    Örnek:
        config = LevelTransitionConfig(
            recent_window_size=5,
            upgrade_threshold=8.5,
            downgrade_threshold=3.5,
        )

    Kullanım:
        service = LevelTransitionService(config=config)

    Domain Notu:
        Bu sınıf business logic içermez.
        Sadece transition kurallarının parametrelerini taşır.

    Architecture:
        Domain/Application boundary içerisinde saf configuration
        objesi olarak davranır.
    """

    recent_window_size: int = WINDOW_SIZE
    """
    Transition kararı için kullanılacak recent score sayısı.

    Amaç:
        Candidate'in anlık tek bir cevabına göre değil,
        kısa dönem performance trend'ine göre karar verebilmek.

    Örnek:
        recent_window_size = 3

        recent_scores:
            [6, 7, 9, 9, 8]

        Kullanılan pencere:
            [9, 9, 8]

    Neden gerekli?
        - noisy evaluation etkisini azaltır
        - daha stabil transition behavior sağlar
        - tek bir kötü cevabın immediate downgrade üretmesini önler
        - adaptive interview pacing oluşturur

    Beklenen:
        Pozitif integer değer olmalıdır.

    Varsayılan:
        3
    """

    upgrade_threshold: float = UPGRADE_THRESHOLD
    """
    Candidate'in bir üst level'a geçebilmesi için gereken
    minimum average score threshold'u.

    Amaç:
        Sustained high performance gösteren candidate'leri
        daha zor seviyelere taşımaktır.

    Örnek:
        upgrade_threshold = 8.0

        recent average:
            8.2 -> upgrade
            7.9 -> no upgrade

    Neden average kullanılır?
        Tek bir yüksek score yerine,
        consistent performance ölçülmek istenir.

    Beklenen:
        0-10 arası float değer.

    Varsayılan:
        8.0
    """

    downgrade_threshold: float = DOWNGRADE_THRESHOLD
    """
    Candidate'in mevcut level'da zorlandığını gösterecek
    minimum performance threshold'u.

    Average score bu değerin altına düşerse
    candidate daha düşük level'a geçirilir.

    Amaç:
        Candidate overload oluşmasını önlemek
        ve interview pacing'i stabilize etmektir.

    Örnek:
        downgrade_threshold = 4.0

        recent average:
            3.5 -> downgrade
            4.2 -> no downgrade

    Neden gerekli?
        - aşırı zor interview flow'unu önler
        - candidate confidence collapse riskini azaltır
        - adaptive questioning stratejisini destekler

    Beklenen:
        0-10 arası float değer.

    Varsayılan:
        4.0
    """


    def __post_init__(self) -> None:
        """
        Config değerlerinin domain açısından güvenli olup olmadığını doğrular.

        Amaç:
            Invalid config state'lerinin sistem içerisine girmesini engellemek.
        
        Doğrulanan kurallar:
            - recent_window_size pozitif integer olmalıdır
            - upgrade_threshold 0-10 arasında olmalıdır
            - downgrade_threshold 0-10 arasında olmalıdır
            - downgrade_threshold upgrade_threshold'dan düşük olmalıdır
        
        Raises:
            ValueError:
                - recent_window_size pozitif integer değilse
                - upgrade_threshold 0-10 arasında değilse
                - downgrade_threshold 0-10 arasında değilse
                - downgrade_threshold upgrade_threshold'dan düşük değilse

        Domain Notu:
            Bu sınıf business logic içermez.
            Sadece transition kurallarının parametrelerini taşır.

        Architecture:
            Domain/Application boundary içerisinde saf configuration objesi olarak davranır.
        """

        if self.recent_window_size <= 0:
            raise ValueError(
                "recent_window_size must be greater than 0."
            )

        if not 0 <= self.downgrade_threshold <= 10:
            raise ValueError(
                "downgrade_threshold must be between 0 and 10."
            )

        if not 0 <= self.upgrade_threshold <= 10:
            raise ValueError(
                "upgrade_threshold must be between 0 and 10."
            )

        if self.downgrade_threshold >= self.upgrade_threshold:
            raise ValueError(
                "downgrade_threshold must be lower than upgrade_threshold."
            )