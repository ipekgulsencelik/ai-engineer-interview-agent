from dataclasses import dataclass, field


@dataclass(frozen=True)
class InterviewCoverage:
    """
    Interview coverage durumunu temsil eden domain model.

    Bu model ileride diversity scoring, pacing, fatigue prevention ve
    telemetry sistemleri için temel veri sağlar.
    """

    covered_categories: set[str] = field(default_factory=set)
    covered_levels: set[str] = field(default_factory=set)
    covered_question_types: set[str] = field(default_factory=set)

    def has_category(self, category: str) -> bool:
        return category in self.covered_categories

    def has_level(self, level: str) -> bool:
        return level in self.covered_levels

    def has_question_type(self, question_type: str) -> bool:
        return question_type in self.covered_question_types
