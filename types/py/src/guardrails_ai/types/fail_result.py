from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from guardrails_ai.types.error_span import ErrorSpan


class FailResult(BaseModel):
    """The output of a validator when validation fails."""

    outcome: Optional[str]
    error_message: str = Field(alias="errorMessage")
    fix_value: Optional[Any] = Field(default=None, alias="fixValue")
    error_spans: Optional[List[ErrorSpan]] = Field(default=None, alias="errorSpans")
    metadata: Optional[Dict[str, Any]] = None
    validated_chunk: Optional[Any] = Field(default=None, alias="validatedChunk")

    model_config = {"validate_by_alias": True, "validate_by_name": True}
