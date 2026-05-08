from dataclasses import dataclass, field

from src.domain.enums.level import Level


@dataclass(frozen=True)
class ScoringContext:
    """
    Soru seçimi ve scoring işlemleri sırasında kullanılan bağlam bilgisidir.

    Bu model adayın mevcut seviyesini, CV becerilerini, daha önce sorulan
    soruları, son skorlarını ve zayıf alanlarını merkezi şekilde taşır.
    """

    current_level: Level | str = "JR"
    cv_skills: list[str] = field(default_factory=list)
    asked_question_ids: list[str] = field(default_factory=list)
    recent_scores: list[float] = field(default_factory=list)
    weak_areas: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        try:
            object.__setattr__(self, "current_level", Level(self.current_level))
        except ValueError as exc:
            raise ValueError(
                f"Invalid current level: {self.current_level}. "
                f"Expected one of: {[level.value for level in Level]}"
            ) from exc

        for score in self.recent_scores:
            if score < 0 or score > 10:
                raise ValueError("Recent scores must be between 0 and 10.")
