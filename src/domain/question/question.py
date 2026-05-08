from dataclasses import dataclass

from src.domain.enums.level import Level
from src.domain.enums.question_type import QuestionType


@dataclass(frozen=True)
class Question:
    """
    Interview sisteminde adaya sorulabilecek tek bir soruyu temsil eden
    immutable domain model.

    Bu model, question bank içindeki her sorunun sistem tarafından
    standart ve güvenli şekilde temsil edilmesini sağlar.

    Amaç:
        Sistemde kullanılan her soru için ortak bir veri yapısı oluşturmak.

    Question modeli şu katmanlarda kullanılabilir:
        - question repository
        - question selection service
        - scoring engine
        - evaluator
        - interview pipeline
        - coverage tracking
        - semantic similarity
        - follow-up chaining

    Neden domain model olarak ayrı tutuluyor?
        Çünkü soru bilgisi yalnızca bir JSON objesi değildir.
        Interview sisteminin karar mekanizmasını etkileyen temel domain
        varlıklarından biridir.

    Neden frozen=True?
        Question nesnesi oluşturulduktan sonra değiştirilmemelidir.

        Bunun avantajları:
            - domain state daha güvenli olur
            - beklenmeyen mutation hataları azalır
            - testler daha deterministic çalışır
            - scoring sırasında aynı soru objesi değişmez kalır
            - repository'den gelen veri güvenilir hale gelir

    Alanlar:
        id:
            Sorunun unique identifier değeridir.

            Örnek:
                "rag_jr_001"
                "embedding_mid_002"
                "evaluation_senior_003"

        text:
            Adaya gösterilecek asıl soru metnidir.

        category:
            Sorunun ait olduğu teknik alanı ifade eder.

            Örnek:
                "RAG"
                "Vector DB & Embedding"
                "LLM Evaluation"
                "Prompt Engineering"

        level:
            Sorunun hedef zorluk seviyesidir.

            Geçerli değerler:
                - JR
                - MID
                - SENIOR

        difficulty:
            Sorunun 1 ile 3 arasındaki mikro zorluk seviyesidir.

            Örnek:
                1 -> kolay
                2 -> orta
                3 -> zor

            Not:
                level genel deneyim seviyesini,
                difficulty ise aynı level içindeki ince zorluk derecesini
                temsil eder.

        question_type:
            Sorunun formatını belirtir.

            Geçerli değerler:
                - conceptual
                - coding
                - scenario

        expected_points:
            Aday cevabında beklenen ana noktaları tutar.

            Evaluator bu listeyi rubric üretirken kullanabilir.

        keywords:
            Soruyla ilişkili önemli kavramları tutar.

            Kullanım alanları:
                - rule-based evaluation
                - semantic search
                - keyword coverage
                - missing keyword analysis

        market_weight:
            Sorunun güncel iş piyasasındaki önemini temsil eder.

            0 ile 1 arasında olmalıdır.

            Örnek:
                0.9 -> çok kritik / piyasada sık aranan konu
                0.5 -> orta önem
                0.1 -> düşük öncelik

        followup_allowed:
            Bu soru üzerinden follow-up question üretimine izin verilip
            verilmediğini belirtir.

            True ise:
                LLM veya pipeline bu soruya bağlı takip sorusu üretebilir.

            False ise:
                Bu soru üzerinden follow-up zinciri başlatılmamalıdır.

    Validation:
        __post_init__ içerisinde model oluşturulduktan hemen sonra temel
        domain kuralları kontrol edilir.

        Böylece geçersiz Question nesneleri sistemin içine giremez.

    Önemli tasarım notu:
        Bu model infrastructure detayları içermez.

        Yani burada:
            - JSON dosya yolu
            - database id formatı
            - API response bilgisi
            - embedding vector
            - ChromaDB metadata

        bulunmamalıdır.

        Bu model saf domain bilgisini temsil eder.
    """

    id: str
    text: str
    category: str
    level: Level | str
    difficulty: int
    question_type: QuestionType | str
    expected_points: list[str]
    keywords: list[str]
    market_weight: float = 0.5
    followup_allowed: bool = True

    def __post_init__(self) -> None:
        """
        Question nesnesi oluşturulduktan sonra domain validation kurallarını
        çalıştırır.

        Dataclass yapısında __init__ otomatik oluşturulur.
        __post_init__ ise otomatik __init__ tamamlandıktan hemen sonra çağrılır.

        Bu methodun amacı:
            - boş id oluşmasını engellemek
            - boş soru metni oluşmasını engellemek
            - boş category oluşmasını engellemek
            - geçersiz level değerini reddetmek
            - geçersiz difficulty değerini reddetmek
            - geçersiz question_type değerini reddetmek
            - market_weight aralığını korumak

        Neden validation burada?
            Çünkü Question bir domain modeldir.
            Domain model kendi geçerlilik kurallarını korumalıdır.

            Böylece JSON repository, test factory veya başka bir kaynak
            yanlış veri üretse bile model kendini korur.

        Raises:
            ValueError:
                Domain kurallarından biri ihlal edildiğinde fırlatılır.
        """

        # ---------------------------------------------------------
        # ID VALIDATION
        # ---------------------------------------------------------
        # Her question benzersiz ve boş olmayan bir id'ye sahip olmalıdır.
        # Bu id:
        #   - repository lookup
        #   - asked question tracking
        #   - interview memory
        #   - semantic similarity karşılaştırmaları
        # için kritik öneme sahiptir.
        if not self.id.strip():
            raise ValueError("Question id cannot be empty.")

        # ---------------------------------------------------------
        # TEXT VALIDATION
        # ---------------------------------------------------------
        # Soru metni boş olamaz.
        # Çünkü adayın göreceği ve evaluator'ın değerlendireceği ana içerik
        # bu alandır.
        if not self.text.strip():
            raise ValueError("Question text cannot be empty.")

        # ---------------------------------------------------------
        # CATEGORY VALIDATION
        # ---------------------------------------------------------
        # Category boş olamaz.
        # Category bilgisi:
        #   - coverage tracking
        #   - diversity scoring
        #   - weak area detection
        #   - question filtering
        # için kullanılır.
        if not self.category.strip():
            raise ValueError("Question category cannot be empty.")

        # ---------------------------------------------------------
        # LEVEL VALIDATION
        # ---------------------------------------------------------
        # Level yalnızca sistemin desteklediği sabit değerlerden biri olabilir.
        # Bu kontrol sayesinde "Junior", "jr", "middle", "senior-level" gibi
        # normalize edilmemiş veya hatalı değerler erken aşamada yakalanır.
        try:
            object.__setattr__(self, "level", Level(self.level))
        except ValueError as exc:
            raise ValueError(
                f"Invalid question level: {self.level}. "
                f"Expected one of: {[level.value for level in Level]}"
            ) from exc

        # ---------------------------------------------------------
        # DIFFICULTY VALIDATION
        # ---------------------------------------------------------
        # Difficulty 1-3 aralığında tutulur.
        # Bu alan level'dan bağımsız olarak mikro zorluk ayarı sağlar.
        #
        # Örnek:
        #   JR + difficulty=1  -> başlangıç seviyesi kolay soru
        #   JR + difficulty=3  -> JR seviyesi için zorlayıcı soru
        #   MID + difficulty=2 -> orta seviye dengeli soru
        if self.difficulty < 1 or self.difficulty > 3:
            raise ValueError("Question difficulty must be between 1 and 3.")

        # ---------------------------------------------------------
        # QUESTION TYPE VALIDATION
        # ---------------------------------------------------------
        # question_type sadece desteklenen soru formatlarından biri olabilir.
        #
        # conceptual:
        #   Teorik bilgi ve kavram anlayışı ölçülür.
        #
        # coding:
        #   Kodlama, algoritma veya implementation becerisi ölçülür.
        #
        # scenario:
        #   Gerçek dünya problemi üzerinden tasarım ve karar verme becerisi ölçülür.
        try:
            object.__setattr__(self, "question_type", QuestionType(self.question_type))
        except ValueError as exc:
            raise ValueError(
                f"Invalid question type: {self.question_type}. "
                f"Expected one of: "
                f"{[question_type.value for question_type in QuestionType]}"
            ) from exc

        # ---------------------------------------------------------
        # MARKET WEIGHT VALIDATION
        # ---------------------------------------------------------
        # market_weight 0 ile 1 arasında normalize edilmiş bir değer olmalıdır.
        #
        # Bu değer scoring engine tarafından sorunun piyasa önceliğini
        # hesaplamak için kullanılabilir.
        #
        # 0.0 -> piyasa açısından düşük öncelik
        # 1.0 -> piyasa açısından çok yüksek öncelik
        if self.market_weight < 0 or self.market_weight > 1:
            raise ValueError("Market weight must be between 0 and 1.")
