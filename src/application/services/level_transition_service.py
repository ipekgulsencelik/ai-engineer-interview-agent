from src.domain.enums.level import Level
from src.domain.policy.level_transition_policy import (
    LevelTransitionPolicy,
)
from src.domain.validators.level_transition_validator import (
    LevelTransitionValidator,
)


class LevelTransitionService:
    """
    Level transition orchestration işlemini yöneten application service.

    Bu service'in temel amacı:
        - input normalize etmek
        - validation çalıştırmak
        - transition policy'yi çağırmak
        - sonucu orchestration seviyesinde yönetmek

    ---------------------------------------------------------
    ARCHITECTURAL ROLE
    ---------------------------------------------------------

    Bu sınıf business rule sahibi değildir.

    Business decision logic:
        -> LevelTransitionPolicy içinde bulunur.

    Validation logic:
        -> LevelTransitionValidator içinde bulunur.

    Bu service yalnızca:
        - workflow orchestration
        - dependency coordination
        - input normalization

    işlemlerini yapar.

    ---------------------------------------------------------
    WHY SEPARATE SERVICE?
    ---------------------------------------------------------

    Çünkü:
        - orchestration ile business logic ayrılmalıdır
        - SRP korunmalıdır
        - testability artmalıdır
        - maintainability güçlenmelidir

    Bu yaklaşım:
        Clean Architecture ve SOLID prensiplerine uygundur.

    ---------------------------------------------------------
    RESPONSIBILITIES
    ---------------------------------------------------------

    Bu service:
        ✔ current level normalize eder
        ✔ validation çalıştırır
        ✔ policy çağırır
        ✔ sonucu döndürür

    Bu service:
        ✘ scoring üretmez
        ✘ evaluator çağırmaz
        ✘ persistence yönetmez
        ✘ telemetry/logging yapmaz
        ✘ question seçmez
    """

    def __init__(
        self,
        policy: LevelTransitionPolicy | None = None,
        validator: LevelTransitionValidator | None = None,
    ) -> None:
        """
        LevelTransitionService nesnesini başlatır.

        Args:
            policy:
                Transition business rule'lerini yöneten policy nesnesi.

            validator:
                Input validation işlemlerini yöneten validator nesnesi.

        Neden dependency injection?
            Çünkü:
                - mocking kolaylaşır
                - unit testing sadeleşir
                - farklı implementation'lar kolay değiştirilir
                - loose coupling sağlanır
        """

        self.policy = policy or LevelTransitionPolicy()

        self.validator = (
            validator or LevelTransitionValidator()
        )

    def transition(
        self,
        *,
        current_level: Level | str,
        recent_scores: list[float],
    ) -> Level:
        """
        Candidate'in yeni interview level'ını belirler.

        Workflow:
            1. current_level normalize edilir
            2. recent_scores validate edilir
            3. transition policy çalıştırılır
            4. yeni level döndürülür

        Args:
            current_level:
                Candidate'in mevcut seviyesi.

                String veya Level enum olabilir.

            recent_scores:
                Candidate'in recent evaluation skorları.

        Returns:
            Level:
                Transition sonrası oluşan yeni level.

        Raises:
            ValueError:
                Geçersiz level gönderilirse.

            TypeError:
                Invalid recent_scores tipi gönderilirse.

        Example:
            service = LevelTransitionService()

            new_level = service.transition(
                current_level=Level.JR,
                recent_scores=[8, 9, 8],
            )

            print(new_level)

            # Output:
            # Level.MID
        """

        # ---------------------------------------------------------
        # LEVEL NORMALIZATION
        # ---------------------------------------------------------
        # Raw input string olsa bile
        # sistem içinde standard enum representation kullanılır.
        level = self._normalize_level(
            current_level,
        )

        # ---------------------------------------------------------
        # VALIDATION
        # ---------------------------------------------------------
        # Invalid domain state oluşmadan önce
        # input integrity doğrulanır.
        self.validator.validate_recent_scores(
            recent_scores,
        )

        # ---------------------------------------------------------
        # POLICY EXECUTION
        # ---------------------------------------------------------
        # Asıl business transition kararı policy tarafından verilir.
        return self.policy.decide(
            current_level=level,
            recent_scores=recent_scores,
        )

    @staticmethod
    def _normalize_level(
        value: Level | str,
    ) -> Level:
        """
        Raw level değerini normalize eder.

        Amaç:
            Sistem içerisinde consistent enum representation kullanmak.

        Args:
            value:
                Raw level değeri.

        Returns:
            Level:
                Normalize edilmiş enum değeri.

        Raises:
            ValueError:
                Geçersiz level değeri gönderildiğinde.

        Example:
            "JR"
                -> Level.JR

            Level.MID
                -> Level.MID
        """

        try:
            return Level(value)

        except ValueError as exc:
            raise ValueError(
                f"Invalid level: {value}"
            ) from exc