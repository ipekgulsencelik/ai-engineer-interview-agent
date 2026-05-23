from __future__ import annotations


class SkillNormalizer:
    """
    Skill normalization helper.
    """

    @staticmethod
    def normalize_many(
        *,
        skills: tuple[str, ...],
    ) -> set[str]:
        normalized_skills: set[str] = set()

        for skill in skills:
            if not isinstance(skill, str):
                raise TypeError(
                    "skills must contain strings."
                )

            normalized = (
                skill.strip().lower()
            )

            if normalized:
                normalized_skills.add(
                    normalized,
                )

        return normalized_skills