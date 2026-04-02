from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, List, Optional
from guardrails_ai.types.fail_result import FailResult


class ReAsk(BaseModel):
    """Represents a pending reask when validation fails and retries are exhausted."""

    incorrect_value: Optional[Any] = Field(default=None, alias="incorrectValue")
    fail_results: Optional[List[FailResult]] = Field(default=None, alias="failResults")

    model_config = {
        "validate_by_alias": True,
        "validate_by_name": True,
        "extra": "allow",
    }
