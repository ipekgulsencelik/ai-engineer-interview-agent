from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class CVSkillExtractionPromptBuilder(
    Protocol,
):
    """
    Candidate profile extraction prompt builder contract.
    """

    def build(
        self,
        *,
        cv_text: str,
    ) -> str:
        """
        CV text üzerinden candidate profile extraction prompt üretir.
        """