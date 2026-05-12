from src.application.factories.selection_result_factory import (
    SelectionResultFactory,
)
from src.application.services.ranking.candidate_question_ranker import (
    CandidateQuestionRanker,
)
from src.domain.entities.question import Question
from src.domain.filtering.candidate_filter import CandidateFilter
from src.domain.scoring.scoring_context import ScoringContext


class QuestionSelectionServiceValidator:
    """
    QuestionSelectionService için dependency ve input validation
    kurallarını yöneten validator sınıfıdır.

    Bu validator'ın temel amacı:
        QuestionSelectionService orchestration sürecine giren dependency
        ve runtime input değerlerinin güvenli, tutarlı ve beklenen domain
        contract'lara uygun olduğunu garanti etmektir.

    ----------------------------------------------------------------------
    QUESTION SELECTION SERVICE NEDİR?
    ----------------------------------------------------------------------

    QuestionSelectionService genellikle tüm question selection pipeline'ını
    orkestre eden üst application service'tir.

    Tipik pipeline akışı:

        questions
            ↓
        filtering
            ↓
        ranking
            ↓
        selection result building
            ↓
        SelectionResult

    Bu pipeline içerisinde QuestionSelectionService:
        - CandidateFilter'ı çağırır
        - CandidateQuestionRanker'ı çağırır
        - SelectionResultBuilder'ı çağırır
        - final SelectionResult üretimini koordine eder

    Bu validator:
        bu orchestration başlamadan önce gerekli dependency ve input
        kontrollerini yapar.

    ----------------------------------------------------------------------
    VALIDATION KAPSAMI
    ----------------------------------------------------------------------

    Bu validator iki ana kategori validate eder:

        1. Dependency validation
            - ranker
            - filterer
            - result_builder

        2. Runtime input validation
            - questions
            - context

    Dependency validation:
        service constructor seviyesinde kullanılmalıdır.

    Runtime input validation:
        public method çağrıları öncesinde kullanılmalıdır.

    ----------------------------------------------------------------------
    NEDEN AYRI VALIDATOR VAR?
    ----------------------------------------------------------------------

    QuestionSelectionService zaten orchestration responsibility taşır.

    Eğer validation logic doğrudan service içinde büyürse:

        - service sınıfı kalabalıklaşır
        - SRP zayıflar
        - validation tekrarları oluşabilir
        - test kapsamı karmaşıklaşır
        - dependency contract'ları dağınık hale gelir

    Bu nedenle validation ayrı bir sınıfa alınır.

    Böylece:
        - QuestionSelectionService sade kalır
        - validation centralized olur
        - fail-fast behavior sağlanır
        - test edilebilirlik artar
        - dependency contract'ları netleşir

    ----------------------------------------------------------------------
    DEFENSIVE DOMAIN PROGRAMMING
    ----------------------------------------------------------------------

    Python dynamically typed bir dil olduğu için runtime'da invalid input
    veya dependency geçilmesi mümkündür.

    Örneğin:

        ranker = None
        filterer = object()
        result_builder = {}
        questions = [{"id": "q1"}]
        context = None

    gibi durumlar pipeline'da daha sonra belirsiz runtime hatalara neden
    olabilir.

    Bu validator:
        invalid state'i pipeline başlangıcında yakalar.

    ----------------------------------------------------------------------
    DESIGN PRINCIPLES
    ----------------------------------------------------------------------

    Bu validator şu prensipleri destekler:

        - fail-fast validation
        - explicit dependency contracts
        - SRP
        - clean orchestration layer
        - testable validation logic
        - application service safety

    ----------------------------------------------------------------------
    BU VALIDATOR NE YAPMAZ?
    ----------------------------------------------------------------------

    Bu validator:

        ✘ filtering yapmaz
        ✘ ranking yapmaz
        ✘ scoring yapmaz
        ✘ selection result oluşturmaz
        ✘ persistence işlemi yapmaz
        ✘ fallback strategy çalıştırmaz

    Sadece:
        QuestionSelectionService input/dependency safety sağlar.
    """

    @staticmethod
    def validate_ranker(
        ranker: CandidateQuestionRanker,
    ) -> None:
        """
        CandidateQuestionRanker dependency'sini validate eder.

        ranker:
            Candidate question listesini skorlayıp RankedCandidate
            listesine dönüştüren application service'tir.

        Bu dependency:
            QuestionSelectionService pipeline'ında ranking aşamasını
            temsil eder.

        Eğer invalid ranker verilirse:
            service orchestration sırasında ranker.rank(...) çağrısı
            başarısız olur.

        Bu nedenle constructor seviyesinde fail-fast validation yapılması
        doğru yaklaşımdır.

        Raises:
            TypeError:
                ranker geçerli CandidateQuestionRanker instance'ı değilse.
        """

        if not isinstance(ranker, CandidateQuestionRanker):
            raise TypeError(
                "ranker must be a CandidateQuestionRanker instance."
            )

    @staticmethod
    def validate_filterer(
        filterer: CandidateFilter,
    ) -> None:
        """
        CandidateFilter dependency'sini validate eder.

        filterer:
            candidate question pool üzerine filtering strategy zinciri
            uygulayan domain service'tir.

        Bu dependency:
            QuestionSelectionService pipeline'ındaki filtering aşamasını
            temsil eder.

        Eğer invalid filterer verilirse:
            service orchestration sırasında filterer.apply(...) çağrısı
            başarısız olur.

        Raises:
            TypeError:
                filterer geçerli CandidateFilter instance'ı değilse.
        """

        if not isinstance(filterer, CandidateFilter):
            raise TypeError(
                "filterer must be a CandidateFilter instance."
            )

    @staticmethod
    def validate_result_builder(
        result_builder: SelectionResultFactory,
    ) -> None:
        """
        SelectionResultFactory dependency'sini validate eder.

        result_builder:
            RankedCandidate listesinden final SelectionResult oluşturan
            factory'dir.

        Bu dependency:
            QuestionSelectionService pipeline'ındaki final result creation
            aşamasını temsil eder.

        Eğer invalid factory verilirse:
            service orchestration sonunda SelectionResult üretimi
            başarısız olur.

        Raises:
            TypeError:
                result_builder geçerli SelectionResultFactory instance'ı
                değilse.
        """

        if not isinstance(result_builder, SelectionResultFactory):
            raise TypeError(
                "result_builder must be a SelectionResultFactory instance."
            )

    @staticmethod
    def validate_questions(
        questions: list[Question],
    ) -> None:
        """
        QuestionSelectionService'e gelen initial question pool'u validate eder.

        Validation kuralları:

            1. questions list olmalıdır.
            2. questions boş olmamalıdır.
            3. Listedeki tüm item'lar Question instance'ı olmalıdır.

        ------------------------------------------------------------------
        NEDEN EMPTY LIST REDDEDİLİYOR?
        ------------------------------------------------------------------

        QuestionSelectionService finalde bir SelectionResult üretmek için
        çalışır.

        Bunun için başlangıçta en az bir candidate question gerekir.

        Eğer questions boşsa:
            filtering, ranking ve selection pipeline semantic olarak
            çalışamaz.

        Bu nedenle burada boş liste invalid state kabul edilir.

        Not:
            Daha alt katmanlarda bazı servisler empty list'i kabul edebilir.

            Örneğin:
                CandidateQuestionRanker boş liste için [] döndürebilir.

            Ancak QuestionSelectionService daha üst orchestration service
            olduğu için final result üretme contract'ı gereği empty input'u
            reddedebilir.

        Raises:
            TypeError:
                questions list değilse veya item'lar Question değilse.

            ValueError:
                questions boşsa.
        """

        if not isinstance(questions, list):
            raise TypeError(
                "questions must be a list."
            )

        if not questions:
            raise ValueError(
                "questions cannot be empty."
            )

        for question in questions:
            if not isinstance(question, Question):
                raise TypeError(
                    "All questions must be Question instances."
                )

    @staticmethod
    def validate_context(
        context: ScoringContext,
    ) -> None:
        """
        QuestionSelectionService'e gelen ScoringContext nesnesini validate eder.

        ScoringContext:
            adaptive question selection sürecinde scoring engine tarafından
            kullanılan contextual domain snapshot'tır.

        Genellikle:
            - current level
            - asked question ids
            - recent scores
            - weak areas
            - cv skills
            - fatigue state

        gibi bilgileri taşıyabilir.

        Eğer context invalid ise:
            scoring ve ranking behavior doğru çalışamaz.

        Raises:
            TypeError:
                context geçerli ScoringContext instance'ı değilse.
        """

        if not isinstance(context, ScoringContext):
            raise TypeError(
                "context must be a ScoringContext instance."
            )