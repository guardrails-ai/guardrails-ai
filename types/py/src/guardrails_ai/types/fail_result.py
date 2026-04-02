from __future__ import annotations
from pydantic import Field, field_validator
from typing import Any, List, Literal, Optional
from guardrails_ai.types.error_span import ErrorSpan
from guardrails_ai.types.validation_result import ValidationResult, Outcome


class FailResult(ValidationResult):
    """The output of a validator when validation fails."""

    outcome: Outcome = Outcome.FAIL
    error_message: str = Field(alias="errorMessage")
    fix_value: Optional[Any] = Field(default=None, alias="fixValue")
    error_spans: Optional[List[ErrorSpan]] = Field(
        default=None,
        alias="errorSpans",
        description="Segments that caused validation to fail. May not exist for non-streamed output.",
    )

    @field_validator("outcome")
    @classmethod
    def deserialize_outcome(cls, outcome: str | None) -> Literal[Outcome.FAIL]:
        return Outcome.FAIL
