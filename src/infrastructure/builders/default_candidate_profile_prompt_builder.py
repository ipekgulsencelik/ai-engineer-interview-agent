from __future__ import annotations

from src.application.constants.prompts.candidate_profile_extraction_prompt_template import (
    CANDIDATE_PROFILE_EXTRACTION_PROMPT_TEMPLATE,
)
from src.application.ports.cv_skill_extraction_prompt_builder import (
    CVSkillExtractionPromptBuilder,
)


class DefaultCVSkillExtractionPromptBuilder(
    CVSkillExtractionPromptBuilder,
):
    """
    Default candidate profile extraction prompt builder.
    """

    def build(
        self,
        *,
        cv_text: str,
    ) -> str:
        return (
            CANDIDATE_PROFILE_EXTRACTION_PROMPT_TEMPLATE.format(
                cv_text=cv_text,
            )
        )