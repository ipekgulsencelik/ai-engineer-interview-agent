class LevelTransitionValidator:
    """
    Level transition input validation kurallarını yöneten utility class.

    Amaç:
        LevelTransitionService içerisine invalid veya corrupted data
        girişini engellemek.

    Bu validator:
        - recent score listesinin tip güvenliğini doğrular
        - score değerlerinin domain kurallarına uygunluğunu kontrol eder
        - invalid state oluşmasını engeller

    Neden ayrı sınıf?
        Validation logic'in service/business flow'dan ayrılması:

            - SRP (Single Responsibility Principle) sağlar
            - test edilebilirliği artırır
            - reusable validation yapısı oluşturur
            - service class'ı sadeleştirir

    Architecture:
        Stateless utility validator olarak tasarlanmıştır.

    Not:
        Bu sınıf business decision vermez.
        Sadece input integrity doğrulaması yapar.
    """

    @staticmethod
    def validate_recent_scores(
        scores: list[float],
    ) -> None:
        """
        Recent interview score listesini doğrular.

        Doğrulanan kurallar:
            1. scores bir list olmalıdır
            2. tüm elemanlar numeric olmalıdır
            3. bool değerler kabul edilmez
            4. score aralığı 0-10 arasında olmalıdır

        Amaç:
            Transition logic çalışmadan önce
            invalid domain state oluşmasını önlemek.

        Args:
            scores:
                Candidate'in recent evaluation score listesi.

                Örnek:
                    [7.5, 8.0, 9.0]

        Raises:
            TypeError:
                - scores list değilse
                - liste numeric olmayan değer içeriyorsa
                - bool değer içeriyorsa

            ValueError:
                - score değeri 0-10 aralığı dışındaysa

        Neden bool reject ediliyor?
            Python'da bool, int subclass'ıdır:
                isinstance(True, int) -> True
            Bu nedenle explicit bool rejection gerekir.

        Domain Rule:
            Interview score sistemi yalnızca
            0-10 arası numeric değer kabul eder.

        Example:
            validator.validate_recent_scores(
                [8.0, 7.5, 9.0]
            )

        Invalid Examples:
            [8, "bad", 9]
            [True, 7, 8]
            [12, 5, 6]
        """

        if not isinstance(scores, list):
            raise TypeError(
                "recent_scores must be a list."
            )

        for score in scores:
            """
            Bool rejection kritik önemlidir.

            Çünkü:
                isinstance(True, int) == True

            Bu yüzden yalnızca numeric kontrolü
            yeterli değildir.
            """
            if isinstance(score, bool) or not isinstance(
                score,
                int | float,
            ):
                raise TypeError(
                    "recent_scores must contain numbers."
                )

            """
            Domain score range validation.

            Interview evaluation sistemi:
                minimum -> 0
                maximum -> 10

            dışında score kabul etmez.
            """
            if score < 0 or score > 10:
                raise ValueError(
                    "Scores must be between 0 and 10."
                )