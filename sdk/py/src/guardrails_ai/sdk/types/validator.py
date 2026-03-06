from guardrails_ai.sdk.types.on_fail import OnFail
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, List, Optional


class Validator(BaseModel):
    """
    Validator
    """

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

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)
