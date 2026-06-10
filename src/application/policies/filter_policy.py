from abc import ABC, abstractmethod

from src.domain.entities.question import Question


class FilterPolicy(ABC):
    """
    Candidate question filtering davranışları için abstract domain
    policy contract'ıdır.

    Bu abstraction'ın temel amacı:
        Question filtering logic'ini orchestration katmanından ayırmak
        ve filtering behavior'un interchangeable policy yapısıyla
        yönetilmesini sağlamaktır.

    ----------------------------------------------------------------------
    FILTERING NEDİR?
    ----------------------------------------------------------------------

    Interview/question selection pipeline'larında genellikle başlangıçta
    büyük bir candidate question pool bulunur.

    Örneğin:
        - retrieval sonucu gelen sorular
        - category bazlı sorular
        - semantic similarity ile bulunan candidate'lar
        - tüm question bank

    Ancak bu soruların tamamı selection aşamasına gönderilmez.

    Önce belirli filtering kuralları uygulanır.

    Örneğin:

        - daha önce sorulmuş soruları elemek
        - yanlış level'daki soruları çıkarmak
        - duplicate candidate'ları temizlemek
        - fatigue-sensitive soruları azaltmak
        - category cooldown uygulamak

    gibi işlemler yapılabilir.

    İşte bu filtering davranışları:
        FilterPolicy abstraction'ı ile modellenir.

    ----------------------------------------------------------------------
    NEDEN POLICY ABSTRACTION VAR?
    ----------------------------------------------------------------------

    Filtering behavior zamanla değişebilir.

    Eğer filtering logic doğrudan service/orchestration içine gömülürse:

        - tightly coupled architecture oluşur
        - filtering rule'ları büyür
        - test etmek zorlaşır
        - reusable yapı kaybolur
        - Open/Closed Principle ihlal edilir

    Bu nedenle policy abstraction kullanılır.

    Böylece:
        - filtering logic interchangeable hale gelir
        - yeni filtering rule'ları kolay eklenir
        - orchestration concrete implementation bilmez
        - dependency inversion sağlanır

    ----------------------------------------------------------------------
    GELECEK POLİCİLER
    ----------------------------------------------------------------------

    Bu abstraction gelecekte farklı filtering implementasyonlarını
    desteklemek için intentionally extensible tasarlanmıştır.

    Örneğin:

        - UnaskedQuestionFilterPolicy
        - DifficultyFilterPolicy
        - CategoryCooldownFilterPolicy
        - DiversityFilterPolicy
        - FatigueAwareFilterPolicy
        - DuplicateQuestionFilterPolicy     
        - SemanticSimilarityFilterPolicy
        - SkillGapFilterPolicy

    gibi concrete policy'ler oluşturulabilir.

    Böylece filtering pipeline:
        composable architecture ile çalışabilir.

    ----------------------------------------------------------------------
    DOMAIN CONTRACT
    ----------------------------------------------------------------------

    Bu abstraction şunu garanti eder:

        "Bir filtering policy uygulandığında, output question listesi yalnızca
        belirli filtering kurallarına göre input question listesinden elenmiş:
            question pool alır
            filtering rule uygular
            yeni filtered question listesi döndürür."

    Bu contract:
        tüm filtering implementasyonları için ortak davranış standardıdır.

    ----------------------------------------------------------------------
    IMMUTABILITY YAKLAŞIMI
    ----------------------------------------------------------------------

    apply method'u:
        mevcut question listesini mutate etmemelidir.

    Bunun yerine:
        yeni filtered liste döndürmelidir.

    Bu yaklaşım:
        - side effect riskini azaltır
        - debugging'i kolaylaştırır
        - pipeline composability sağlar
        - deterministic behavior üretir

    ----------------------------------------------------------------------
    BU SINIFIN SORUMLULUKLARI
    ----------------------------------------------------------------------

    Bu abstraction:

        ✔ filtering contract tanımlar
        ✔ policy polymorphism sağlar
        ✔ interchangeable filtering architecture oluşturur
        ✔ orchestration ile filtering'i decouple eder

    Bu abstraction:

        ✘ scoring yapmaz
        ✘ ranking yapmaz
        ✘ selection kararı vermez
        ✘ orchestration yönetmez
        ✘ persistence işlemi yapmaz
        ✘ retrieval işlemi yapmaz

    ----------------------------------------------------------------------
    POLICY PATTERN
    ----------------------------------------------------------------------

    Bu yapı klasik Policy Pattern implementasyonudur.

    Orchestration/service katmanı:

        policy.apply(...)

    çağrısı yapar ancak hangi filtering davranışının çalıştığını
    bilmek zorunda değildir.

    Böylece runtime'da filtering behavior kolayca değiştirilebilir.

    ----------------------------------------------------------------------
    TYPE SAFETY
    ----------------------------------------------------------------------

    Filtering policy yalnızca Question entity listesi ile çalışır.

    Çünkü filtering:
        scoring ve ranking'den önce çalışan pipeline aşamasıdır.

    Henüz:
        - RankedCandidate
        - SelectionResult
        - score breakdown

    gibi yapılar oluşmamıştır.

    Bu separation:
        pipeline stage'lerini netleştirir.
    """

    @abstractmethod
    def apply(
        self,
        *,
        questions: list[Question],
        asked_question_ids: set[str],
    ) -> list[Question]:
        """
        Verilen question pool üzerine filtering rule uygular.

        Bu method:
            tüm concrete FilterPolicy implementasyonları için
            zorunlu filtering contract'ıdır.

        Her concrete policy kendi filtering behavior'unu bu method içinde implemente eder.

        ------------------------------------------------------------------
        FILTERING PIPELINE
        ------------------------------------------------------------------

        Filtering işlemi genellikle selection pipeline'ın erken
        aşamalarında çalışır.

        Amaç:
            gereksiz veya unsuitable candidate'ları
            scoring/ranking aşamasına göndermemektir.

        Bu:
            - computational efficiency sağlar
            - ranking quality artırır
            - pipeline complexity azaltır

        ------------------------------------------------------------------
        INPUT CONTRACT
        ------------------------------------------------------------------

        questions:
            Candidate question pool.

            Bu liste:
                - retrieval sonucu oluşmuş olabilir
                - repository'den gelmiş olabilir
                - semantic search sonucu olabilir

        asked_question_ids:
            Daha önce candidate'a sorulmuş question ID'leri.

            Özellikle:
                repeated question filtering
            için kullanılır.

        ------------------------------------------------------------------
        OUTPUT CONTRACT
        ------------------------------------------------------------------

        Method:
            filtering uygulanmış yeni bir question listesi döndürmelidir.

        Beklenen davranış:

            input:
                [q1, q2, q3, q4]

            output:
                [q1, q3]

        Orijinal liste mutate edilmemelidir.

        ------------------------------------------------------------------
        GELECEK GENİŞLEME
        ------------------------------------------------------------------

        İleride strategy implementasyonları:

            - semantic filtering
            - adaptive filtering
            - contextual filtering
            - probabilistic filtering
            - multi-stage filtering

        gibi daha gelişmiş davranışlar uygulayabilir.

        Bu nedenle contract intentionally generic tutulmuştur.

        ------------------------------------------------------------------
        Args
        ------------------------------------------------------------------

        questions:
            Filtering uygulanacak candidate question listesi.

        asked_question_ids:
            Daha önce sorulmuş question ID kümesi.

        ------------------------------------------------------------------
        Returns
        ------------------------------------------------------------------

        list[Question]:
            Filtering sonrası kalan question listesi.

        ------------------------------------------------------------------
        Not
        ------------------------------------------------------------------

        Bu method:
            sorting yapmamalıdır.

        Çünkü filtering ve ranking farklı pipeline sorumluluklarıdır.
        """
        raise NotImplementedError()