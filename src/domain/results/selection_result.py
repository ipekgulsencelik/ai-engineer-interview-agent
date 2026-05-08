from dataclasses import dataclass

from src.domain.question.question import Question
from src.domain.results.scoring_signals import (
    ScoringSignals,
)


@dataclass(frozen=True)
class SelectionResult:
    """
    Question selection işleminin sonucunu temsil eden immutable domain model.

    Bu modelin amacı:
        Question selection pipeline'ının çıktısını explainable ve structured
        şekilde temsil etmektir.

    Neden ayrı bir SelectionResult modeli gerekiyor?
        Çünkü production-grade selection sistemlerinde yalnızca:
            "hangi soru seçildi?"

        bilgisi yeterli değildir.

        Sistem aynı zamanda:
            - neden bu sorunun seçildiğini
            - hangi scoring sinyallerinin etkili olduğunu
            - final skorun nasıl oluştuğunu

        da açıklayabilmelidir.

    Bu model sayesinde selection:
        ✔ explainable olur
        ✔ debug edilebilir hale gelir
        ✔ analytics üretilebilir
        ✔ telemetry desteklenir
        ✔ ranking davranışı analiz edilebilir
        ✔ UI explanation gösterilebilir

    Problem örneği:
        Eğer sadece:
            Question

        döndürülürse:

            "Bu soru neden seçildi?"

        sorusunun cevabı kaybolur.

    Ancak SelectionResult ile:
        - selected question
        - final score
        - scoring breakdown

        birlikte taşınabilir.

    Örnek:
        SelectionResult(
            question=...,
            final_score=0.91,
            signals=ScoringSignals(
                level_score=0.8,
                market_score=0.9,
            ),
        )

    Böylece:
        - explainability artar
        - observability güçlenir
        - ranking debugging kolaylaşır

    Neden frozen=True?
        Çünkü selection sonucu immutable bir snapshot olarak düşünülmelidir.

        Yani:
            belirli bir interview anında
            belirli bir context ile
            belirli bir soru seçildi

        bilgisini temsil eder.

        Sonradan mutate edilmesi:
            - analytics corruption
            - inconsistent telemetry
            - debugging problemleri
            - nondeterministic behavior

        oluşturabilir.

    Kullanım alanları:
        - QuestionSelectionService
        - InterviewPipeline
        - telemetry
        - ranking analytics
        - selection explanation UI
        - interview replay/debugging
        - adaptive interview analysis

    Bu model hangi bilgileri taşır?
        question:
            Seçilen Question domain modeli.

        final_score:
            Selection sırasında hesaplanan birleşik skor.

        signals:
            Final skoru oluşturan scoring bileşenleri.

    Mimari yaklaşım:
        SelectionResult:
            selection outcome snapshot'ıdır.

        Şunları içermez:
            ✘ scoring algorithm implementation
            ✘ evaluator state
            ✘ persistence logic
            ✘ retrieval orchestration

        Çünkü bunlar farklı katmanların sorumluluğudur.

    Gelecekte eklenebilecek alanlar:
        - ranking_position
        - candidate_count
        - rejected_reasons
        - selection_latency
        - retrieval_metadata
        - diversity_breakdown
        - semantic_matches
        - exploration_probability

    Example:
        result = SelectionResult(
            question=question,
            final_score=0.92,
            signals=signals,
        )

        print(result.question.text)
        print(result.final_score)

    Output:
        "Explain how RAG works."
        0.92
    """

    # ---------------------------------------------------------
    # SELECTED QUESTION
    # ---------------------------------------------------------
    # Selection pipeline sonucunda seçilen Question domain modelidir.
    #
    # Bu alan:
    #   - UI rendering
    #   - interview flow
    #   - evaluator input
    #   - telemetry
    #
    # için kullanılabilir.
    #
    # Question modeli:
    #   - text
    #   - level
    #   - category
    #   - difficulty
    #   - market_weight
    #
    # gibi selection açısından kritik bilgileri içerir.
    question: Question

    # ---------------------------------------------------------
    # FINAL COMBINED SCORE
    # ---------------------------------------------------------
    # Question'ın selection sırasında aldığı toplam skor.
    #
    # Bu skor:
    #   scoring engine tarafından üretilir.
    #
    # Daha yüksek skor:
    #   → daha uygun question
    #
    # Daha düşük skor:
    #   → daha düşük selection priority
    #
    # Kullanım alanları:
    #   - ranking visualization
    #   - telemetry
    #   - debugging
    #   - analytics
    #   - threshold filtering
    final_score: float

    # ---------------------------------------------------------
    # SCORING BREAKDOWN SIGNALS
    # ---------------------------------------------------------
    # Final score'u oluşturan scoring bileşenlerini temsil eder.
    #
    # Bu alan explainability açısından kritiktir.
    #
    # Örnek:
    #   level_score:
    #       0.9
    #
    #   market_score:
    #       0.8
    #
    #   fatigue_score:
    #       -0.2
    #
    # Böylece:
    #   "Bu soru neden seçildi?"
    #
    # sorusu açıklanabilir hale gelir.
    #
    # Bu yapı:
    #   - observability
    #   - tuning
    #   - analytics
    #   - ranking debugging
    #
    # için production-grade foundation sağlar.
    signals: ScoringSignals
