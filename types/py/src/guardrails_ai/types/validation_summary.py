from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from guardrails_ai.types.error_span import ErrorSpan


class ValidationSummary(BaseModel):
    """Per-validator result produced during a Guard execution."""

    validator_name: str = Field(
        description="The class name of the validator.", alias="validatorName"
    )
    validator_status: Literal["pass"] | Literal["fail"] = Field(alias="validatorStatus")
    property_path: Optional[str] = Field(
        default=None,
        description="The JSON path to the property which was validated that produced this log.",
        alias="propertyPath",
    )
    failure_reason: Optional[str] = Field(
        default=None,
        description="The error message indicating why validation failed.",
        alias="failureReason",
    )
    error_spans: Optional[List[ErrorSpan]] = Field(default=None, alias="errorSpans")

    model_config = {"validate_by_alias": True, "validate_by_name": True}
