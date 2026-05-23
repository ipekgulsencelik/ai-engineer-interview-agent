from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class CVSkillExtractionPromptBuilder(
    Protocol,
):
    """
    Candidate profile extraction prompt builder contract.

    Bu contract:
        - raw CV text üzerinden extraction prompt üretimini tanımlar
        - application katmanını concrete prompt strategy
          implementasyonlarından izole eder
        - farklı extraction prompting stratejilerinin
          interchangeable olmasını sağlar
    """

    def build(
        self,
        *,
        cv_text: str,
    ) -> str:
        """
        Candidate profile extraction prompt üretir.

        Args:
            cv_text:
                Extract edilmiş raw CV text.

        Returns:
            LLM-compatible extraction prompt.
        """