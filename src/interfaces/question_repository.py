from abc import ABC, abstractmethod

from src.domain.question.question import Question


class QuestionRepository(ABC):
    """
    Question persistence/retrieval layer için repository contract'ı.

    Bu sınıf doğrudan veri okuyan somut bir repository değildir.
    Bunun yerine soru verisinin nereden ve nasıl okunacağını soyutlayan
    ortak bir interface tanımlar.

    Amaç:
        Application/service katmanının JSON, database, API veya başka bir
        storage teknolojisine doğrudan bağımlı olmasını engellemektir.

    İlk aşamada:
        - JsonQuestionRepository

    kullanılabilir.

    İlerleyen fazlarda:
        - DatabaseQuestionRepository
        - ApiQuestionRepository
        - VectorBackedQuestionRepository
        - CachedQuestionRepository
        - InMemoryQuestionRepository

    gibi farklı implementasyonlar aynı contract üzerinden sisteme eklenebilir.

    Neden repository interface kullanıyoruz?
        - Veri kaynağı değişse bile servis katmanı değişmez.
        - Dependency Inversion Principle uygulanır.
        - Testlerde fake/in-memory repository kullanılabilir.
        - JSON'dan database'e geçiş kolaylaşır.
        - QuestionSelectionService veri okuma detaylarından izole edilir.
        - Persistence logic domain logic ile karışmaz.

    Mimari konum:
        Service/Application layer:
            QuestionSelectionService
            QuestionRetrievalService

        Interface:
            QuestionRepository

        Infrastructure implementations:
            JsonQuestionRepository
            DatabaseQuestionRepository
            InMemoryQuestionRepository

    Önemli tasarım notu:
        Bu interface sadece question retrieval contract'ını tanımlar.

        Burada:
            - JSON dosyası açma
            - database connection yönetimi
            - API request atma
            - cache invalidation
            - file path yönetimi
            - ORM detayları

        bulunmamalıdır.

        Bu detaylar somut repository implementasyonlarında tutulmalıdır.

    Beklenen davranış:
        Repository, dış veri kaynağından Question domain model'lerini döndürür.

        Yani servis katmanı raw dict, JSON object veya database row ile değil,
        doğrudan Question domain modeli ile çalışır.

    Not:
        Bu interface şu an read-only tasarlanmıştır.

        Çünkü Faz 1 kapsamında ihtiyaç:
            - tüm soruları listelemek
            - id ile soru bulmak

        seviyesindedir.

        İleride admin panel veya question management özelliği eklenirse:
            - save
            - update
            - delete
            - search_by_category
            - list_by_level

        gibi methodlar ayrı interface veya genişletilmiş repository üzerinden
        eklenebilir.
    """

    @abstractmethod
    def list_all(self) -> list[Question]:
        """
        Repository içerisindeki tüm soruları döndürür.

        Bu method, question selection pipeline'ının başlangıç noktalarından
        biridir.

        QuestionSelectionService genellikle:
            1. Repository'den tüm soruları alır.
            2. Daha önce sorulmuş soruları filtreler.
            3. Level/category/type gibi kuralları uygular.
            4. ScoringEngine ile her soruya skor verir.
            5. En uygun soruyu seçer.

        Returns:
            list[Question]:
                Sistemde kayıtlı tüm Question domain modellerinin listesi.

                Boş liste dönebilir.
                Bu durum repository'nin çalışmadığı anlamına gelmek zorunda
                değildir; veri kaynağında henüz soru olmayabilir.

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan QuestionRepository
                üzerinden çağrılamaz. Mutlaka somut bir subclass tarafından
                implemente edilmelidir.

            RuntimeError:
                Somut implementasyonlar dosya okuma, database bağlantısı veya
                API hatalarını uygulama seviyesinde anlamlı hatalara
                dönüştürebilir.

        Design Note:
            Bu method raw JSON/dict döndürmemelidir.

            Doğru dönüş:
                list[Question]

            Yanlış dönüş:
                list[dict]
                list[str]
                raw database rows

            Böylece domain katmanı tutarlı kalır.
        """
        pass

    @abstractmethod
    def get_by_id(self, question_id: str) -> Question | None:
        """
        Verilen ID'ye göre tek bir Question döndürür.

        Bu method, spesifik bir soruya erişmek gereken durumlarda kullanılır.

        Örnek kullanım senaryoları:
            - Daha önce sorulan bir question id'sinden question detayını bulmak
            - Testlerde belirli bir soruyu çekmek
            - UI tarafında question detail göstermek
            - Follow-up chaining için parent question'ı bulmak
            - Interview memory içinde referanslanan soruyu resolve etmek

        Args:
            question_id:
                Aranacak Question modelinin unique identifier değeridir.

                Örnek:
                    "rag_jr_001"
                    "embedding_mid_003"
                    "eval_senior_002"

                Boş string olmamalıdır.
                Somut implementasyonlar boş id durumunda ValueError
                fırlatabilir.

        Returns:
            Question | None:
                ID eşleşirse ilgili Question domain modeli döner.

                ID bulunamazsa None döner.

                None dönmesi normal ve beklenen bir durumdur.
                Bu sayede servis katmanı:
                    - soru bulunamadı senaryosunu kontrollü yönetebilir
                    - özel hata fırlatabilir
                    - fallback davranış uygulayabilir

        Raises:
            NotImplementedError:
                Bu method abstract olduğu için doğrudan QuestionRepository
                üzerinden çağrılamaz. Mutlaka somut bir subclass tarafından
                implemente edilmelidir.

            ValueError:
                Somut implementasyonlar boş veya geçersiz question_id için
                ValueError fırlatabilir.

            RuntimeError:
                Veri kaynağına erişim sırasında oluşan teknik hatalar
                somut repository tarafından RuntimeError gibi uygulama
                seviyesinde anlamlı hatalara dönüştürülebilir.

        Design Note:
            Bu method exception yerine bulunamama durumunda None döndürür.

            Çünkü "id yok" durumu teknik bir hata değil, domain açısından
            beklenebilir bir sonuçtur.

            Ancak veri kaynağı okunamıyorsa, dosya bozuksa veya database
            bağlantısı başarısızsa bu teknik hata olarak ele alınmalıdır.
        """
        pass
