from dataclasses import dataclass, field


@dataclass(frozen=True)
class SelectionExplanation:
    """
    Bir sorunun neden seçildiğini açıklayan domain model.

    Bu model debug, observability ve kullanıcıya açıklanabilir seçim mantığı
    sunmak için kullanılır.
    """

    question_id: str
    final_score: float
    reasons: list[str] = field(default_factory=list)
    signals: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise ValueError("Question id cannot be empty.")

        if self.final_score < 0:
            raise ValueError("Final score cannot be negative.")
