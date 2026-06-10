from src.domain.entities.question import Question
from src.domain.validators.candidate_filter_validator import (
    CandidateFilterValidator,
)
from src.domain.policies.filter_policy import (
    FilterPolicy,
)


class UnaskedQuestionFilterPolicy(FilterPolicy):
    """
    Daha önce sorulmuş question'ları candidate pool'dan çıkaran
    concrete filtering policy implementasyonudur.

    Bu policy'nin temel amacı:
        Candidate'a daha önce sorulmuş soruların tekrar selection
        pipeline'ına girmesini engellemektir.

    ----------------------------------------------------------------------
    PROBLEM TANIMI
    ----------------------------------------------------------------------

    Interview/question selection sistemlerinde aynı soruların tekrar tekrar
    sorulması ciddi kalite problemleri oluşturabilir.

    Örneğin:
        - candidate experience düşebilir
        - interview diversity azalabilir
        - skill coverage zayıflayabilir
        - adaptive interview davranışı bozulabilir
        - learning signal kalitesi düşebilir

    Bu nedenle:
        daha önce sorulmuş sorular candidate pool'dan filtrelenir.

    ----------------------------------------------------------------------
    POLICY DAVRANIŞI
    ----------------------------------------------------------------------

    Bu policy oldukça deterministik çalışır.

    Filtering kuralı:

        question.id not in asked_question_ids

    şeklindedir.

    Yani:
        question.id değeri daha önce sorulmuş ID set'i içinde varsa
        ilgili question candidate pool'dan çıkarılır.

    ----------------------------------------------------------------------
    NEDEN SET KULLANILIYOR?
    ----------------------------------------------------------------------

    asked_question_ids:
        set[str] olarak modellenmiştir.

    Çünkü filtering işlemi membership lookup ağırlıklıdır.

    Örneğin:

        if question.id in asked_question_ids

    gibi kontroller yapılır.

    set veri yapısı:
        average O(1) lookup performansı sağlar.

    Eğer list kullanılsaydı:
        lookup işlemi O(n) olurdu.

    Büyük question pool'larda bu performans problemi oluşturabilir.

    ----------------------------------------------------------------------
    IMMUTABILITY YAKLAŞIMI
    ----------------------------------------------------------------------

    Bu policy input listesini mutate etmez.

    Bunun yerine:
        yeni filtered liste üretir.

    Bu yaklaşımın avantajları:

        - side effect riskini azaltır
        - pipeline composability sağlar
        - debugging kolaylaşır
        - deterministic behavior üretir
        - functional-style filtering sağlar

    ----------------------------------------------------------------------
    PIPELINE ROLÜ
    ----------------------------------------------------------------------

    Bu policy genellikle selection pipeline'ın erken aşamalarında çalışır.

    Pipeline örneği:

        retrieval
            ↓
        filtering
            ↓
        scoring
            ↓
        ranking
            ↓
        selection

    Amaç:
        gereksiz question'ları scoring/ranking aşamasına göndermemektir.

    Bu:
        - computational efficiency sağlar
        - ranking quality artırır
        - duplicate interview riskini azaltır

    ----------------------------------------------------------------------
    GELECEK GENİŞLEME
    ----------------------------------------------------------------------

    Bu policy yalnızca "daha önce sorulmuş mu?"
    kuralını uygular.

    Ancak gelecekte farklı filtering policy'leri eklenebilir:

        - DifficultyFilterPolicy
        - DiversityFilterPolicy
        - FatigueAwareFilterPolicy
        - SemanticSimilarityFilterPolicy
        - CooldownFilterPolicy

    CandidateFilter orchestration katmanı:
        bu policy'leri chain halinde çalıştırabilir.

    ----------------------------------------------------------------------
    BU SINIFIN SORUMLULUKLARI
    ----------------------------------------------------------------------

    Bu policy:

        ✔ previously asked question filtering yapar
        ✔ filtering contract'ını implemente eder
        ✔ reusable filtering behavior sağlar
        ✔ immutable filtering sonucu üretir

    Bu policy:

        ✘ scoring yapmaz
        ✘ ranking yapmaz
        ✘ sorting yapmaz
        ✘ final selection kararı vermez
        ✘ orchestration yönetmez
        ✘ candidate oluşturmaz

    ----------------------------------------------------------------------
    DOMAIN CONTRACT
    ----------------------------------------------------------------------

    Bu policy şunu garanti eder:

        "Output question listesi yalnızca daha önce sorulmamış
        question'lardan oluşur."

    Bu:
        interview diversity açısından kritik business invariant'tır.
    """

    def apply(
        self,
        *,
        questions: list[Question],
        asked_question_ids: set[str],
    ) -> list[Question]:
        """
        Daha önce sorulmuş question'ları candidate pool'dan filtreler.

        Filtering kuralı:

            question.id not in asked_question_ids

        şeklindedir.

        ------------------------------------------------------------------
        VALIDATION
        ------------------------------------------------------------------

        Filtering başlamadan önce input validation yapılır.

        Validation kapsamında:

            - questions gerçekten list mi?
            - listedeki item'lar Question mı?
            - asked_question_ids gerçekten set mi?
            - set içindeki item'lar string mi?

        kontrolleri uygulanır.

        Böylece filtering logic:
            güvenli domain input ile çalışır.

        ------------------------------------------------------------------
        FILTERING DAVRANIŞI
        ------------------------------------------------------------------

        Policy'nin temel davranışı:
            question.id değeri asked_question_ids içinde bulunan
            question'ları eler.

        Örnek:

            questions:
                [q1, q2, q3]

            asked_question_ids:
                {"q2"}

            output:
                [q1, q3]

        ------------------------------------------------------------------
        PERFORMANCE
        ------------------------------------------------------------------

        Membership lookup:

            question.id in asked_question_ids

        set veri yapısı sayesinde average O(1) complexity ile çalışır.

        Bu yaklaşım:
            büyük candidate pool'larda performans avantajı sağlar.

        ------------------------------------------------------------------
        IMMUTABILITY
        ------------------------------------------------------------------

        Method input listesini mutate etmez.

        Bunun yerine:
            yeni filtered liste döndürür.

        Bu:
            safer pipeline behavior sağlar.

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
            Daha önce sorulmamış question'lardan oluşan yeni liste.

        ------------------------------------------------------------------
        Not
        ------------------------------------------------------------------

        Bu method:
            ordering değiştirmez.

        Input listesi hangi sıradaysa:
            output listesi de aynı relative ordering'i korur.

        Yani:
            stable filtering behavior uygulanır.
        """

        CandidateFilterValidator.validate_questions(questions)

        CandidateFilterValidator.validate_asked_question_ids(
            asked_question_ids
        )

        return [
            question
            for question in questions
            if question.id not in asked_question_ids
        ]