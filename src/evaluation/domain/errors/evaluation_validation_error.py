from __future__ import annotations


class EvaluationValidationError(ValueError):
    """
    Evaluation domain validation hatalarını temsil eder.

    Bu exception:
        - evaluation entity validation
        - metric validation
        - alignment validation
        - dataset validation

    sırasında oluşan domain-level validation problemleri için kullanılır.
    """