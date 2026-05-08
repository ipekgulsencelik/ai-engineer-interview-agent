import json
from pathlib import Path

from src.domain.question.question import Question
from src.interfaces.question_repository import (
    QuestionRepository,
)


class JsonQuestionRepository(QuestionRepository):
    """
    JSON tabanlı question repository implementation'ı.

    Bu repository'nin amacı:
        Question verilerini JSON dosyasından okuyarak domain modeli haline
        dönüştürmek ve application katmanına sağlamaktır.

    Repository pattern neden kullanılıyor?
        Çünkü application/business logic:
            verinin nerede tutulduğunu bilmemelidir.

        Verinin:
            - JSON dosyasında
            - PostgreSQL'de
            - MongoDB'de
            - REST API'de
            - vector database'te

        tutulması business logic açısından önemsiz olmalıdır.

    Bu yaklaşım sayesinde:
        ✔ loose coupling sağlanır
        ✔ persistence abstraction oluşur
        ✔ test edilebilirlik artar
        ✔ storage backend kolay değiştirilebilir
        ✔ domain layer izole kalır

    JsonQuestionRepository ne yapar?
        ✔ JSON dosyasını okur
        ✔ raw JSON verisini parse eder
        ✔ Question domain modeli üretir
        ✔ repository contract'ını uygular

    JsonQuestionRepository ne yapmaz?
        ✘ question selection
        ✘ scoring
        ✘ evaluation
        ✘ semantic retrieval
        ✘ vector search
        ✘ caching logic
        ✘ interview orchestration

    Böylece Single Responsibility Principle korunur.

    Mimari konum:
        Application Layer
                ↓
        QuestionRepository interface
                ↓
        JsonQuestionRepository
                ↓
        JSON file storage

    Neden JSON repository ile başlıyoruz?
        Çünkü Faz-1 için:
            - hızlı geliştirme
            - düşük complexity
            - kolay debugging
            - kolay inspection

        avantajları sağlar.

    JSON yaklaşımının avantajları:
        ✔ human-readable
        ✔ git-friendly
        ✔ hızlı prototyping
        ✔ kolay backup/versioning
        ✔ dependency gerektirmez

    Dezavantajları:
        ✘ büyük veri setlerinde yavaş olabilir
        ✘ concurrency desteği zayıftır
        ✘ query capability sınırlıdır
        ✘ indexing yoktur

    Bu tradeoff Faz-1 için bilinçli olarak kabul edilmiştir.

    Gelecekte eklenebilecek repository implementasyonları:
        - PostgresQuestionRepository
        - MongoQuestionRepository
        - ChromaQuestionRepository
        - PineconeQuestionRepository
        - HybridQuestionRepository
        - CachedQuestionRepository

    Önemli tasarım notu:
        Repository:
            raw dict döndürmez.

        Bunun yerine:
            Question domain modeli döndürür.

        Çünkü domain layer:
            persistence formatı değil,
            domain object'leri ile çalışmalıdır.

    JSON örnek formatı:
        [
            {
                "id": "rag_jr_001",
                "text": "What is RAG?",
                "category": "RAG",
                "level": "JR",
                "difficulty": 1,
                "question_type": "conceptual",
                "expected_points": [...],
                "keywords": [...],
                "market_weight": 0.8
            }
        ]
    """

    def __init__(self, json_path: str) -> None:
        """
        JsonQuestionRepository instance'ı oluşturur.

        Args:
            json_path:
                Question JSON dosyasının filesystem path'i.

                Örnek:
                    "data/questions.json"

        Design Note:
            Path abstraction kullanılması bilinçlidir.

            pathlib.Path:
                - platform bağımsızdır
                - daha güvenlidir
                - daha okunabilirdir
                - modern Python yaklaşımıdır

            os.path yerine tercih edilir.
        """

        # ---------------------------------------------------------
        # PATH NORMALIZATION
        # ---------------------------------------------------------
        # String path pathlib.Path nesnesine dönüştürülür.
        #
        # Böylece:
        #   - filesystem operasyonları daha güvenli olur
        #   - platform compatibility artar
        #   - path manipulation kolaylaşır
        self.json_path = Path(json_path)

    def list_all(self) -> list[Question]:
        """
        JSON dosyasındaki tüm question kayıtlarını yükler.

        Akış:
            1. JSON dosyasının varlığı kontrol edilir.
            2. Dosya okunur.
            3. JSON parse edilir.
            4. Raw dict verileri Question domain modeline dönüştürülür.
            5. Question listesi döndürülür.

        Returns:
            list[Question]:
                JSON içerisindeki tüm question kayıtlarının domain model
                listesi.

        Raises:
            FileNotFoundError:
                JSON dosyası mevcut değilse fırlatılır.

            json.JSONDecodeError:
                JSON malformed ise fırlatılabilir.

            KeyError:
                Zorunlu field'lar eksikse oluşabilir.

            ValueError:
                Question domain validation başarısız olursa oluşabilir.

        Design Note:
            Repository:
                raw dict döndürmez.

            Bunun yerine Question domain modeli üretir.

            Böylece:
                - domain validation otomatik çalışır
                - invalid state erken yakalanır
                - application layer type-safe çalışır

        Example:
            repository = JsonQuestionRepository(
                "data/questions.json"
            )

            questions = repository.list_all()

            print(len(questions))
        """

        # ---------------------------------------------------------
        # FILE EXISTENCE CHECK
        # ---------------------------------------------------------
        # JSON dosyasının gerçekten mevcut olup olmadığı doğrulanır.
        #
        # Bu kontrol:
        #   - invalid path problemlerini
        #   - deployment issue'larını
        #   - config hatalarını
        #
        # erken aşamada yakalar.
        if not self.json_path.exists():
            raise FileNotFoundError(f"Question file not found: {self.json_path}")

        # ---------------------------------------------------------
        # FILE READING
        # ---------------------------------------------------------
        # JSON dosyası UTF-8 encoding ile okunur.
        #
        # UTF-8 seçilmesinin nedeni:
        #   - Türkçe karakter desteği
        #   - Unicode compatibility
        #   - modern standart olması
        #
        # json.load():
        #   raw JSON verisini Python list/dict yapısına dönüştürür.
        with self.json_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            raw_questions = json.load(file)

        # ---------------------------------------------------------
        # DOMAIN MODEL MAPPING
        # ---------------------------------------------------------
        # Raw JSON dict verileri Question domain modeline dönüştürülür.
        #
        # Bu aşama kritik öneme sahiptir çünkü:
        #   - domain validation burada çalışır
        #   - invalid question state burada yakalanır
        #   - application layer artık typed object ile çalışır
        #
        # item.get(...):
        #   Optional field'lar için güvenli fallback sağlar.
        #
        # market_weight:
        #   belirtilmemişse 0.5
        #
        # followup_allowed:
        #   belirtilmemişse True
        return [
            Question(
                id=item["id"],
                text=item["text"],
                category=item["category"],
                level=item["level"],
                difficulty=item["difficulty"],
                question_type=item["question_type"],
                expected_points=item["expected_points"],
                keywords=item["keywords"],
                market_weight=item.get(
                    "market_weight",
                    0.5,
                ),
                followup_allowed=item.get(
                    "followup_allowed",
                    True,
                ),
            )
            for item in raw_questions
        ]

    def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        """
        Verilen ID'ye sahip tek bir Question döndürür.

        Akış:
            1. Tüm question'lar yüklenir.
            2. ID eşleşmesi aranır.
            3. Eşleşen Question döndürülür.
            4. Bulunamazsa None döner.

        Args:
            question_id:
                Aranacak unique question identifier.

                Örnek:
                    "rag_jr_001"

        Returns:
            Question | None:
                Eşleşen Question domain modeli.

                Eğer question bulunamazsa:
                    None

                döndürülür.

        Design Note:
            Bu implementasyon Faz-1 için intentionally basittir.

            Şu an:
                O(n) linear search

            kullanılmaktadır.

            Küçük dataset'ler için yeterlidir.

        Production-scale geliştirmeler:
            - in-memory indexing
            - hashmap lookup
            - database indexing
            - caching
            - lazy loading

        Example:
            question = repository.get_by_id(
                "rag_jr_001"
            )

            if question:
                print(question.text)
        """

        # ---------------------------------------------------------
        # FULL QUESTION LOAD
        # ---------------------------------------------------------
        # Tüm question'lar repository'den yüklenir.
        #
        # Faz-1 için kabul edilebilir basit yaklaşım.
        questions = self.list_all()

        # ---------------------------------------------------------
        # LINEAR SEARCH
        # ---------------------------------------------------------
        # Question listesi içerisinde ID eşleşmesi aranır.
        #
        # İlk eşleşme bulunduğunda hemen return edilir.
        #
        # Çünkü:
        #   question.id unique kabul edilir.
        for question in questions:
            if question.id == question_id:
                return question

        # ---------------------------------------------------------
        # NOT FOUND
        # ---------------------------------------------------------
        # Hiçbir eşleşme bulunamazsa None döndürülür.
        #
        # Bu explicit "not found" davranışıdır.
        return None
