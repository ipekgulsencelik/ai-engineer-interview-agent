from __future__ import annotations

from src.application.ports.cv_skill_extraction_prompt_builder import (
    CVSkillExtractionPromptBuilder,
)


class DefaultCVSkillExtractionPromptBuilder(CVSkillExtractionPromptBuilder):
    """Builds a compact JSON-only prompt for CV skill extraction."""

    def build(
        self,
        *,
        cv_text: str,
    ) -> str:
        return (
            "Extract the candidate profile from this CV. "
            "Return only valid JSON with keys: detected_level, years_of_experience, "
            "skills, weak_skills. detected_level must be JR, MID, or SENIOR.\n\n"
            f"CV:\n{cv_text}"
        )