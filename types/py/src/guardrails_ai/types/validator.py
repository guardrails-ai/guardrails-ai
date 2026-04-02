from __future__ import annotations
from guardrails_ai.types.on_fail import OnFail
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class Validator(BaseModel):
    """A validator attached to a Guard, including its configuration."""

    id: str = Field(
        description="The unique identifier for this Validator.  Often the hub id; e.g. guardrails/regex_match"
    )
    on: Optional[str] = Field(
        default=None,
        description='A reference to the property this validator should be applied against.  Can be a valid JSON path or a meta-property such as "messages" or "output"',
    )
    on_fail: Optional[OnFail] = Field(default=OnFail.NOOP, alias="onFail")
    args: Optional[List[Any]] = None
    kwargs: Dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "validate_by_alias": True,
        "validate_by_name": True,
        "use_enum_values": True,
    }
