from src.domain.question.question import Question
from src.domain.results.pipeline_result import (
    PipelineResult,
)
from src.domain.scoring.scoring_context import ScoringContext
from src.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.services.level_transition_service import (
    LevelTransitionService,
)
from src.services.question_selection_service import (
    QuestionSelectionService,
)


class InterviewPipeline:
    """
    Faz-1 interview orchestration pipeline.

    Bu sınıf interview akışının ana koordinasyon katmanıdır.

    Temel amacı:
        Tek bir interview adımında gerekli servisleri doğru sırayla
        çalıştırmak ve sonucu üst katmana standart
        bir PipelineResult olarak döndürmektir.

    Faz-1 akışı:
        1. Question selection
        2. Answer evaluation
        3. Level transition

    Yani pipeline şu sırayla çalışır:

        question selection
            ↓
        answer evaluation
            ↓
        recent score update
            ↓
        level transition
            ↓
        response oluşturma

    Bu sınıf ne yapar?
        ✔ En uygun soruyu seçtirir
        ✔ Aday cevabını değerlendirir
        ✔ Yeni skor geçmişini oluşturur
        ✔ Bir sonraki seviyeyi hesaplatır
        ✔ Pipeline sonucunu döndürür

    Bu sınıf ne yapmaz?
        ✘ Scoring algoritması yazmaz
        ✘ LLM provider çağrısı yapmaz
        ✘ Level transition kuralını içermez
        ✘ Question repository'den veri çekmez
        ✘ Database işlemi yapmaz
        ✘ UI veya CLI çıktısı üretmez

    Mimari yaklaşım:
        InterviewPipeline bir orchestration layer'dır.

        Business detaylarını servislerin içine dağıtır ve sadece akışı yönetir.

    Mimari konum:
        Presentation Layer:
            CLI / API / UI

                ↓

        Pipeline:
            InterviewPipeline

                ↓

        Application Services:
            QuestionSelectionService
            AnswerEvaluationService
            LevelTransitionService

                ↓

        Interfaces / Implementations:
            ScoringEngine
            Evaluator

    Neden ayrı pipeline sınıfı var?
        Çünkü interview akışı birden fazla service'in birlikte çalışmasını
        gerektirir.

        Eğer bu akış CLI, API veya UI içinde yazılırsa:
            - presentation layer kirlenir
            - test yazmak zorlaşır
            - orchestration logic tekrar eder
            - servisler arası bağımlılık dağılır

        Pipeline sayesinde:
            - use-case tek yerde toplanır
            - test edilebilirlik artar
            - API/CLI/UI aynı akışı kullanabilir
            - ileride LangGraph entegrasyonu kolaylaşır

    Dependency Injection:
        Pipeline ihtiyaç duyduğu servisleri constructor üzerinden alır.

        Böylece:
            - pipeline somut implementasyonlara bağımlı olmaz
            - testlerde mock/fake servis kullanılabilir
            - service composition dışarıdan yönetilebilir

    Faz-2/Faz-3 geliştirme alanları:
        - asked_question_ids güncelleme
        - interview state persistence
        - follow-up question generation
        - coverage update
        - semantic diversity kontrolü
        - adaptive difficulty adjustment
        - LangGraph state machine entegrasyonu
        - telemetry/logging
        - structured response model
        - error handling strategy
    """

    def __init__(
        self,
        question_selection_service: QuestionSelectionService,
        answer_evaluation_service: AnswerEvaluationService,
        level_transition_service: LevelTransitionService,
    ) -> None:
        """
        InterviewPipeline instance'ı oluşturur.

        Args:
            question_selection_service:
                Mevcut context'e göre en uygun soruyu seçen service.

            answer_evaluation_service:
                Seçilen soru ve aday cevabını değerlendirten service.

            level_transition_service:
                Son skor geçmişine göre bir sonraki interview seviyesini
                hesaplayan service.

        Design Note:
            Burada constructor injection kullanılır.

            Pipeline servisleri kendi içinde oluşturmaz.

            Bunun avantajları:
                - loose coupling
                - kolay test edilebilirlik
                - farklı service implementasyonlarıyla çalışma
                - composition root mantığına uygun yapı
        """

        # ---------------------------------------------------------
        # DEPENDENCY INJECTION
        # ---------------------------------------------------------
        # Pipeline doğrudan somut algoritmaları bilmez.
        #
        # Sadece application service'leri koordine eder.
        self.question_selection_service = question_selection_service
        self.answer_evaluation_service = answer_evaluation_service
        self.level_transition_service = level_transition_service

    def run(
        self,
        questions: list[Question],
        context: ScoringContext,
        answer: str,
    ) -> PipelineResult:
        """
        Tek bir interview step'ini çalıştırır.

        Bu method Faz-1 için temel orchestration entry point'tir.

        Akış:
            1. Candidate question listesi içinden en uygun soru seçilir.
            2. Kullanıcının cevabı seçilen soru bağlamında değerlendirilir.
            3. Evaluation score mevcut skor geçmişine eklenir.
            4. Yeni skor geçmişine göre level transition yapılır.
            5. Response dict döndürülür.

        Args:
            questions:
                Selection yapılabilecek candidate question listesi.

            context:
                Mevcut interview state/context bilgisidir.

                Kullanılan alanlar:
                    - current_level
                    - recent_scores
                    - asked_question_ids
                    - cv_skills
                    - weak_areas

            answer:
                Adayın seçilen soruya verdiği cevaptır.

        Returns:
            PipelineResult:
                Interview step sonucunu temsil eden response.

                Dönen alanlar:
                    PipelineResult(
                        question=selected_question.text,
                        score=evaluation_result.score,
                        feedback=evaluation_result.feedback,
                        next_level=next_level,
                    )

        Raises:
            ValueError:
                Alt servislerden gelen validation hataları propagate olabilir.

                Örnek:
                    - available question yoksa
                    - answer boşsa
                    - current_level geçersizse

        Design Note:
            Bu method şu an PipelineResult döndürüyor.

            Faz ilerledikçe InterviewStepResult gibi typed bir dataclass'a
            geçmek daha doğru olur.

            Çünkü typed result:
                - IDE desteğini artırır
                - testleri güçlendirir
                - key typo riskini azaltır
                - API response mapping'i kolaylaştırır
        """

        # ---------------------------------------------------------
        # QUESTION SELECTION
        # ---------------------------------------------------------
        # Mevcut context'e göre en uygun soru seçilir.
        #
        # Selection service:
        #   - daha önce sorulmuş soruları filtreler
        #   - scoring engine ile soruları skorlar
        #   - en yüksek skorlu soruyu döndürür
        selected_question = self.question_selection_service.select_question(
            questions=questions,
            context=context,
        )

        # ---------------------------------------------------------
        # ANSWER EVALUATION
        # ---------------------------------------------------------
        # Adayın cevabı seçilen question bağlamında değerlendirilir.
        #
        # Evaluation service:
        #   - answer validation yapar
        #   - evaluator'a delegasyon yapar
        #   - score/feedback sonucunu döndürür
        evaluation_answer_result = self.answer_evaluation_service.evaluate_answer(
            question=selected_question,
            answer=answer,
        )

        if not evaluation_answer_result.success:
            raise ValueError(evaluation_answer_result.error)

        evaluation_result = evaluation_answer_result.unwrap()

        # ---------------------------------------------------------
        # SCORE HISTORY UPDATE
        # ---------------------------------------------------------
        # Mevcut recent_scores listesi mutate edilmez.
        #
        # Bunun yerine yeni bir liste oluşturulur.
        #
        # Neden?
        #   - context immutable olabilir
        #   - side effect azaltılır
        #   - test/debug davranışı daha güvenli olur
        updated_scores = [
            *context.recent_scores,
            evaluation_result.score,
        ]

        # ---------------------------------------------------------
        # LEVEL TRANSITION
        # ---------------------------------------------------------
        # Güncellenmiş skor geçmişine göre bir sonraki seviye hesaplanır.
        #
        # LevelTransitionService:
        #   - son 3 skor ortalamasını alır
        #   - yüksek performansta level up yapar
        #   - düşük performansta level down yapar
        #   - aksi durumda level'i korur
        next_level = self.level_transition_service.transition(
            current_level=context.current_level,
            recent_scores=updated_scores,
        )

        # ---------------------------------------------------------
        # PIPELINE RESPONSE
        # ---------------------------------------------------------
        # Üst katmanın kullanabileceği sade bir response döndürülür.
        #
        # Bu response CLI, API veya UI tarafında doğrudan gösterilebilir.
        return PipelineResult(
            question=selected_question,
            evaluation=evaluation_result,
            next_level=next_level,
        )
