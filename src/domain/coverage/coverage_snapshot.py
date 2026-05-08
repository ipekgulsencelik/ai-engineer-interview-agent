from dataclasses import dataclass, field


@dataclass(frozen=True)
class CoverageSnapshot:
    """
    Mülakat sürecinde kapsanan category, level ve question type dağılımını
    temsil eden immutable snapshot modelidir.
    """

    category_counts: dict[str, int] = field(default_factory=dict)
    level_counts: dict[str, int] = field(default_factory=dict)
    question_type_counts: dict[str, int] = field(default_factory=dict)

    @property
    def total_questions(self) -> int:
        return sum(self.category_counts.values())
