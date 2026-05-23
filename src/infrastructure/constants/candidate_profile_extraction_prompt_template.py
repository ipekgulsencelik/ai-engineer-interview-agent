from __future__ import annotations

from typing import Final


CANDIDATE_PROFILE_EXTRACTION_PROMPT_TEMPLATE: Final[str] = """
You are an AI Engineering recruiter.

Analyze the following CV.

Extract:
- detected_level (JR/MID/SENIOR)
- skills
- weak_skills
- years_of_experience
- target_roles
- summary
- education
- projects

Return STRICT JSON:

{{
  "detected_level": "JR",
  "skills": [],
  "weak_skills": [],
  "years_of_experience": 0,
  "target_roles": [],
  "summary": null,
  "education": [],
  "projects": []
}}

CV:

{cv_text}
"""