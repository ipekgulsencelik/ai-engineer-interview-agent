from src.domain.enums.level import Level


class LevelTransitionService:
    """
    Adayın performansına göre interview seviyesini yöneten application service.

    Bu service'in amacı:
        Adayın son cevap performanslarını analiz ederek interview seviyesini
        dinamik şekilde güncellemektir.

    Sistem neden level transition yapıyor?
        Çünkü interview süreci statik değil adaptif olmalıdır.

        Örneğin:
            - çok başarılı adaylar daha zor sorulara geçebilmelidir
            - zorlanan adaylar tamamen kilitlenmeden daha uygun seviyeye
              çekilebilmelidir

    Böylece interview:
        - daha gerçekçi
        - daha dengeli
        - daha ölçücü
        - daha kişiselleştirilmiş

    hale gelir.

    Faz-1 yaklaşımı:
        Şu an sistem intentionally basit bir rule-based transition mantığı
        kullanmaktadır.

        Kurallar:
            - Son 3 skor ortalaması >= 8 ise level yükselir
            - Son 3 skor ortalaması <= 4 ise level düşer
            - Diğer durumlarda level korunur

    Örnek:
        recent_scores = [9, 8, 9]
            average = 8.66
            → level up

        recent_scores = [3, 4, 2]
            average = 3.0
            → level down

        recent_scores = [6, 7, 5]
            average = 6.0
            → same level

    Mimari konum:
        Presentation Layer:
            CLI / API / UI

                ↓

        Application Layer:
            LevelTransitionService

                ↓

        Domain:
            level constants
            interview state

    Bu service neden ayrı tutuluyor?
        Çünkü level transition interview orchestration'a ait bir use-case'tir.

        Bu logic:
            - Question modelinde olmamalıdır
            - Evaluator içinde olmamalıdır
            - Selection service içinde olmamalıdır

        Ayrı service olması sayesinde:
            - test edilmesi kolaylaşır
            - transition algoritması bağımsız gelişebilir
            - farklı transition stratejileri eklenebilir

    Gelecekte geliştirilebilecek alanlar:
        Faz-2/Faz-3'te sistem:
            - confidence-aware transition
            - category-specific leveling
            - adaptive difficulty
            - fatigue detection
            - momentum scoring
            - volatility smoothing
            - Bayesian skill estimation
            - reinforcement-based adaptation

        gibi daha gelişmiş mekanizmalara evrilebilir.

    Önemli tasarım notu:
        Bu service sadece level transition kararını verir.

        Şunları yapmamalıdır:
            - soru seçmek
            - evaluator çağırmak
            - scoring üretmek
            - persistence işlemi yapmak
            - telemetry yönetmek

        Bu sayede Single Responsibility Principle korunur.

    LEVEL_ORDER:
        Sistemde desteklenen level progression sırasını tanımlar.

        JR → MID → SENIOR

        Bu sıra:
            - level up/down işlemlerinde
            - boundary kontrolünde
            - progression logic içinde

        kullanılır.
    """

    LEVEL_ORDER = [Level.JR, Level.MID, Level.SENIOR]

    def transition(
        self,
        current_level: Level | str,
        recent_scores: list[float],
    ) -> Level:
        """
        Son interview skorlarına göre yeni level belirler.

        Bu method adayın yakın performans geçmişini analiz eder ve
        mevcut seviyenin:
            - yükseltilip yükseltilmeyeceğine
            - düşürülüp düşürülmeyeceğine
            - korunup korunmayacağına
        karar verir.

        Transition mantığı:
            1. Son 3 skor alınır.
            2. Ortalama hesaplanır.
            3. Ortalama yüksekse level up yapılır.
            4. Ortalama düşükse level down yapılır.
            5. Aksi durumda mevcut level korunur.

        Args:
            current_level:
                Adayın mevcut interview seviyesidir.

                Desteklenen değerler:
                    - JR
                    - MID
                    - SENIOR

                Bu değer:
                    - soru seçiminde
                    - difficulty kontrolünde
                    - adaptive interview flow'da
                kullanılır.

            recent_scores:
                Adayın son evaluation skorlarını içerir.

                Örnek:
                    [7, 8, 9]
                    [3, 4, 5]

                Bu skorlar genellikle evaluator tarafından üretilir.

                Liste boş olabilir.
                Bu durumda sistem mevcut level'i korur.

        Returns:
            Level:
                Yeni interview level değeri.

                Olası dönüşler:
                    - Level.JR
                    - Level.MID
                    - Level.SENIOR

                Level:
                    - yükselebilir
                    - düşebilir
                    - aynı kalabilir

        Raises:
            ValueError:
                current_level sistemde tanımlı geçerli level'lardan biri
                değilse fırlatılır.

        Design Note:
            Son 3 skorun kullanılması bilinçli bir tercihtir.

            Neden?
                Tek bir kötü cevap:
                    → anlık hata olabilir

                Tek bir çok iyi cevap:
                    → şans faktörü olabilir

            Son birkaç skor kullanıldığında:
                - daha stabil transition elde edilir
                - ani level değişimleri azalır
                - interview daha doğal hissettirir

        Example:
            service = LevelTransitionService()

            new_level = service.transition(
                current_level=Level.JR,
                recent_scores=[8, 9, 8]
            )

            print(new_level)

        Output:
            Level.MID
        """

        # ---------------------------------------------------------
        # CURRENT LEVEL VALIDATION
        # ---------------------------------------------------------
        # Sistem yalnızca tanımlı level'larla çalışmalıdır.
        #
        # Bu kontrol:
        #   - typo kaynaklı hataları
        #   - normalize edilmemiş inputları
        #   - invalid state oluşmasını
        # önler.
        #
        # Örneğin:
        #   "junior"
        #   "mid-level"
        #   "expert"
        # gibi değerler geçersiz kabul edilir.
        try:
            level = Level(current_level)
        except ValueError as exc:
            raise ValueError("Invalid current level.") from exc

        # ---------------------------------------------------------
        # EMPTY SCORE HANDLING
        # ---------------------------------------------------------
        # Henüz skor yoksa transition yapmak için yeterli veri yoktur.
        #
        # Bu durumda en güvenli davranış:
        #   mevcut level'i korumaktır.
        #
        # Bu senaryo genellikle:
        #   - interview başlangıcında
        #   - ilk soru öncesinde
        #   - evaluation failure durumlarında
        #
        # ortaya çıkabilir.
        if not recent_scores:
            return level

        # ---------------------------------------------------------
        # RECENT WINDOW SELECTION
        # ---------------------------------------------------------
        # Sadece son 3 skor dikkate alınır.
        #
        # Neden tüm geçmiş değil?
        #   Çünkü sistem adayın güncel performansına daha duyarlı olmalıdır.
        #
        # Örneğin:
        #   eski kötü performanslar sonsuza kadar cezalandırmamalıdır.
        last_scores = recent_scores[-3:]

        # ---------------------------------------------------------
        # PERFORMANCE AVERAGE
        # ---------------------------------------------------------
        # Son skorların ortalaması hesaplanır.
        #
        # Bu ortalama transition kararının ana sinyalidir.
        average_score = sum(last_scores) / len(last_scores)

        # ---------------------------------------------------------
        # CURRENT LEVEL POSITION
        # ---------------------------------------------------------
        # Level sırası içerisindeki mevcut index bulunur.
        #
        # Örnek:
        #   Level.JR      -> 0
        #   Level.MID     -> 1
        #   Level.SENIOR  -> 2
        #
        # Bu index level up/down sırasında kullanılacaktır.
        current_index = self.LEVEL_ORDER.index(level)

        # ---------------------------------------------------------
        # LEVEL UP RULE
        # ---------------------------------------------------------
        # Ortalama skor yüksekse aday mevcut seviyeyi rahat yönetiyor
        # kabul edilir.
        #
        # Bu durumda:
        #   bir üst seviyeye geçilir.
        #
        # Boundary kontrolü:
        #   SENIOR zaten en üst level olduğu için daha yukarı çıkamaz.
        if average_score >= 8 and current_index < len(self.LEVEL_ORDER) - 1:
            return self.LEVEL_ORDER[current_index + 1]

        # ---------------------------------------------------------
        # LEVEL DOWN RULE
        # ---------------------------------------------------------
        # Ortalama skor çok düşükse aday mevcut seviyede zorlanıyor
        # kabul edilir.
        #
        # Bu durumda:
        #   bir alt seviyeye geçilir.
        #
        # Boundary kontrolü:
        #   JR zaten en düşük level olduğu için daha aşağı inemez.
        if average_score <= 4 and current_index > 0:
            return self.LEVEL_ORDER[current_index - 1]

        # ---------------------------------------------------------
        # STABLE LEVEL
        # ---------------------------------------------------------
        # Aday ne çok zorlanıyor ne de mevcut seviyeyi tamamen domine ediyor.
        #
        # Bu durumda mevcut level korunur.
        #
        # Bu yaklaşım:
        #   - interview stabilitesini artırır
        #   - gereksiz level sıçramalarını azaltır
        #   - aday deneyimini daha doğal hale getirir
        return level
