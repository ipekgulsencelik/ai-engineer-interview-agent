from src.domain.entities.question import Question
from src.domain.enums.question_type import QuestionType
from src.domain.interview.question_fatigue import QuestionFatigue
from src.services.fatigue_multiplier_policy import FatigueMultiplierPolicy


class QuestionFatigueService:
    """
    Daha önce sorulmuş sorulardan QuestionFatigue snapshot üreten domain
    service sınıfıdır.

    Bu servis, interview sırasında candidate'ın cognitive fatigue durumunu
    anlamak için son sorulan soruları analiz eder.

    Temel amaç:
        Adaya üst üste:
            - çok zor
            - aynı tipte
            - aynı kategoride
            - system design ağırlıklı

        sorular sorulup sorulmadığını tespit etmek.

    Neden gerekli?
        Teknik interview sistemlerinde soru seçimi yalnızca:
            - market relevance
            - CV gap
            - semantic similarity
            - difficulty matching

        gibi sinyallere göre yapılırsa, aday üzerinde aşırı bilişsel yük
        oluşabilir.

    Örnek problem:
        Son 3 soru şu şekilde olsun:

            1. Senior system design
            2. Senior scalability
            3. Senior distributed systems

        Bu akış teknik olarak alakalı olabilir.
        Ancak candidate için yoğun cognitive overload oluşturabilir.

    QuestionFatigueService bu tür durumları tespit ederek scoring engine'e
    kullanılabilir bir fatigue snapshot sağlar.

    Bu servis ne yapar?
        - recent question window'u belirler
        - yüksek difficulty soru sayısını hesaplar
        - tekrar eden question type sayısını hesaplar
        - tekrar eden category sayısını hesaplar
        - system design soru sayısını hesaplar
        - fatigue multiplier üretmek için policy kullanır
        - QuestionFatigue snapshot döndürür

    Bu servis ne yapmaz?
        - soru seçmez
        - scoring yapmaz
        - fatigue penalty uygulamaz
        - interview state mutate etmez
        - LLM evaluation yapmaz
        - persistence işlemi yapmaz

    Neden service olarak tasarlandı?
        Çünkü QuestionFatigue modeli yalnızca immutable snapshot taşır.

        Fatigue hesaplama logic'i ise bir davranıştır.

        Bu davranış modelin içine konulursa:
            - model şişer
            - state representation ile computation karışır
            - test izolasyonu azalır

        Bu yüzden hesaplama logic'i service içine alınmıştır.

    FatigueMultiplierPolicy neden inject ediliyor?
        Çünkü multiplier hesaplama stratejisi değişebilir.

        Örneğin:
            - threshold-based policy
            - weighted policy
            - ML-based policy
            - candidate-specific adaptive policy

        kullanılabilir.

        Bu servis yalnızca fatigue sinyallerini çıkarır.
        Multiplier stratejisini policy'ye bırakır.

    Bu yaklaşım:
        - Dependency Injection
        - Open/Closed Principle
        - Single Responsibility Principle

    açısından daha temizdir.

    Akış:
        asked_questions
            ↓
        recent window alınır
            ↓
        fatigue signal count'ları hesaplanır
            ↓
        multiplier policy çalıştırılır
            ↓
        QuestionFatigue snapshot döner

    Örnek kullanım:
        service = QuestionFatigueService()

        fatigue = service.build(
            asked_questions=asked_questions,
            recent_window_size=3,
        )

        if fatigue.is_high_fatigue():
            # scoring engine daha hafif soru seçebilir
            ...
    """

    DEFAULT_RECENT_WINDOW_SIZE = 3
    """
    Fatigue hesaplamasında varsayılan olarak dikkate alınacak son soru
    sayısıdır.

    Neden 3?
        Son birkaç soru candidate'ın mevcut bilişsel yükünü anlamak için
        genellikle yeterli bir kısa dönem penceresi sağlar.

    Bu değer:
        - çok küçük olursa fatigue erken yakalanamayabilir
        - çok büyük olursa eski sorular güncel fatigue sinyalini bozabilir

    Bu nedenle 3 makul bir default recent window değeridir.
    """

    HIGH_DIFFICULTY_THRESHOLD = 3
    """
    Yüksek difficulty kabul edilen minimum soru zorluk değeridir.

    Bu projede difficulty genellikle şu şekilde modellenir:

        1 -> kolay
        2 -> orta
        3 -> zor

    Bu nedenle difficulty >= 3 olan sorular high difficulty kabul edilir.
    """

    def __init__(
        self,
        multiplier_policy: FatigueMultiplierPolicy | None = None,
    ) -> None:
        """
        QuestionFatigueService nesnesini oluşturur.

        Args:
            multiplier_policy:
                Fatigue signal count'larından pacing multiplier üretecek
                policy nesnesi.

                None verilirse default FatigueMultiplierPolicy kullanılır.

        Neden dependency injection?
            Çünkü fatigue multiplier hesaplama stratejisi ileride değişebilir.

            Örneğin testlerde custom/mock policy verilebilir:

                QuestionFatigueService(
                    multiplier_policy=FakeFatigueMultiplierPolicy()
                )

            Böylece:
                - servis daha test edilebilir olur
                - policy değişimi kolaylaşır
                - servis concrete strategy'ye gömülmez
        """
        self.multiplier_policy = multiplier_policy or FatigueMultiplierPolicy()

    def build(
        self,
        asked_questions: list[Question],
        recent_window_size: int = DEFAULT_RECENT_WINDOW_SIZE,
    ) -> QuestionFatigue:
        """
        Sorulmuş question listesine göre QuestionFatigue snapshot üretir.

        Bu metod servisin ana public entry-point'idir.

        Input:
            asked_questions:
                Interview boyunca daha önce sorulmuş Question listesi.

            recent_window_size:
                Fatigue hesaplamasında dikkate alınacak son soru sayısı.

        Akış:
            1. recent_window_size validate edilir.
            2. asked_questions içinden son N soru alınır.
            3. high difficulty soru sayısı hesaplanır.
            4. tekrar eden question type sayısı hesaplanır.
            5. tekrar eden category sayısı hesaplanır.
            6. system design soru sayısı hesaplanır.
            7. multiplier policy ile fatigue multiplier hesaplanır.
            8. QuestionFatigue snapshot döndürülür.

        Neden yalnızca recent window kullanılıyor?
            Çünkü fatigue anlık / yakın dönemli bir sinyaldir.

            Interview başında sorulan eski bir zor soru, interview'in ilerleyen
            aşamasındaki güncel cognitive load'u doğrudan temsil etmeyebilir.

        Args:
            asked_questions:
                Daha önce sorulmuş Question nesneleri.

            recent_window_size:
                Son kaç sorunun fatigue analizine dahil edileceği.

        Returns:
            QuestionFatigue:
                Hesaplanmış fatigue signal snapshot'ı.

        Raises:
            ValueError:
                recent_window_size geçersizse fırlatılır.
        """

        self._validate_recent_window_size(recent_window_size)

        recent_questions = self._get_recent_questions(
            asked_questions=asked_questions,
            recent_window_size=recent_window_size,
        )

        high_difficulty_count = self._count_high_difficulty_questions(
            recent_questions,
        )

        repeated_question_type_count = self._count_repeated_question_type(
            recent_questions,
        )

        repeated_category_count = self._count_repeated_category(
            recent_questions,
        )

        system_design_count = self._count_system_design_questions(
            recent_questions,
        )

        fatigue_multiplier = self.multiplier_policy.compute(
            high_difficulty_count=high_difficulty_count,
            repeated_question_type_count=repeated_question_type_count,
            repeated_category_count=repeated_category_count,
            system_design_count=system_design_count,
        )

        return QuestionFatigue(
            high_difficulty_count=high_difficulty_count,
            repeated_question_type_count=repeated_question_type_count,
            repeated_category_count=repeated_category_count,
            system_design_count=system_design_count,
            fatigue_multiplier=fatigue_multiplier,
        )

    def _get_recent_questions(
        self,
        asked_questions: list[Question],
        recent_window_size: int,
    ) -> list[Question]:
        """
        asked_questions listesinden son N soruyu döndürür.

        Bu helper fatigue hesaplamasının yalnızca yakın dönem interview
        penceresine odaklanmasını sağlar.

        Örnek:
            asked_questions = [q1, q2, q3, q4]
            recent_window_size = 3

            çıktı:
                [q2, q3, q4]

        Eğer asked_questions listesi recent_window_size değerinden kısaysa,
        Python slicing mevcut tüm listeyi döndürür.

        Örnek:
            asked_questions = [q1]
            recent_window_size = 3

            çıktı:
                [q1]

        Args:
            asked_questions:
                Interview boyunca sorulmuş tüm question listesi.

            recent_window_size:
                Dikkate alınacak son soru sayısı.

        Returns:
            list[Question]:
                Son N question nesnesi.
        """
        return asked_questions[-recent_window_size:]

    def _count_high_difficulty_questions(
        self,
        questions: list[Question],
    ) -> int:
        """
        Verilen question penceresinde yüksek difficulty seviyesine sahip
        soru sayısını hesaplar.

        High difficulty tanımı:
            question.difficulty >= HIGH_DIFFICULTY_THRESHOLD

        Varsayılan olarak:
            HIGH_DIFFICULTY_THRESHOLD = 3

        Bu ne anlama gelir?
            Difficulty 3 olan sorular zor soru kabul edilir.

        Bu sinyal neden önemli?
            Üst üste zor sorular candidate üzerinde cognitive overload
            oluşturabilir.

        Args:
            questions:
                Fatigue analizi yapılacak recent question listesi.

        Returns:
            int:
                High difficulty soru sayısı.
        """
        return sum(
            1
            for question in questions
            if question.difficulty >= self.HIGH_DIFFICULTY_THRESHOLD
        )

    def _count_repeated_question_type(
        self,
        questions: list[Question],
    ) -> int:
        """
        Listenin sonundan başlayarak art arda aynı question_type'a sahip
        soru sayısını hesaplar.

        Bu metod özellikle son soruların monotonlaşıp monotonlaşmadığını
        tespit etmek için kullanılır.

        Örnek:
            questions:
                [conceptual, debugging, debugging, debugging]

            çıktı:
                3

        Çünkü son 3 soru aynı question_type'a sahiptir.

        Neden sadece son ardışık tekrarlar sayılıyor?
            Çünkü fatigue açısından en önemli sinyal yakın zamanda üst üste
            gelen tekrarları yakalamaktır.

            Liste içinde dağınık şekilde aynı type bulunması daha düşük
            fatigue etkisine sahiptir.

        Args:
            questions:
                Fatigue analizi yapılacak recent question listesi.

        Returns:
            int:
                Sondan başlayarak tekrar eden question_type sayısı.
        """
        if not questions:
            return 0

        last_type = questions[-1].question_type

        count = 0

        for question in reversed(questions):
            if question.question_type != last_type:
                break

            count += 1

        return count

    def _count_repeated_category(
        self,
        questions: list[Question],
    ) -> int:
        """
        Listenin sonundan başlayarak art arda aynı category değerine sahip
        soru sayısını hesaplar.

        Örnek:
            questions:
                [RAG, MLOps, RAG, RAG]

            çıktı:
                2

        Çünkü son iki soru aynı category'ye aittir.

        Bu sinyal neden önemli?
            Interview'in üst üste aynı kategoriye sıkışması:
                - değerlendirme kapsamını daraltır
                - candidate için repetitive deneyim oluşturur
                - coverage diversity'yi düşürür

        Args:
            questions:
                Fatigue analizi yapılacak recent question listesi.

        Returns:
            int:
                Sondan başlayarak tekrar eden category sayısı.
        """
        if not questions:
            return 0

        last_category = questions[-1].category

        count = 0

        for question in reversed(questions):
            if question.category != last_category:
                break

            count += 1

        return count

    def _count_system_design_questions(
        self,
        questions: list[Question],
    ) -> int:
        """
        Verilen recent question penceresindeki system design soru sayısını
        hesaplar.

        System design neden ayrı takip ediliyor?
            Çünkü system design soruları genellikle:
                - uzun reasoning
                - architecture trade-off analizi
                - scalability düşüncesi
                - component design
                - failure mode değerlendirmesi

            gerektirir.

        Bu nedenle üst üste çok fazla system design sorusu candidate için
        yüksek bilişsel yük oluşturabilir.

        Args:
            questions:
                Fatigue analizi yapılacak recent question listesi.

        Returns:
            int:
                System design question sayısı.
        """
        return sum(
            1
            for question in questions
            if question.question_type == QuestionType.SYSTEM_DESIGN
        )

    @staticmethod
    def _validate_recent_window_size(
        recent_window_size: int,
    ) -> None:
        """
        recent_window_size parametresini doğrular.

        Kurallar:
            - int olmalıdır
            - bool kabul edilmez
            - 0'dan büyük olmalıdır

        Neden bool reddediliyor?
            Python'da bool, int'in subclass'ıdır.

            Yani:
                isinstance(True, int) == True

            Ancak:
                recent_window_size=True

            domain açısından anlamsızdır.

        Args:
            recent_window_size:
                Fatigue analizinde dikkate alınacak son soru sayısı.

        Raises:
            ValueError:
                recent_window_size integer değilse veya 0'dan küçük/eşitse
                fırlatılır.
        """
        if isinstance(recent_window_size, bool) or not isinstance(
            recent_window_size,
            int,
        ):
            raise ValueError("recent_window_size must be an integer.")

        if recent_window_size <= 0:
            raise ValueError("recent_window_size must be greater than 0.")