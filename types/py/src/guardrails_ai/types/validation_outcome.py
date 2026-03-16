from __future__ import annotations
from typing import Dict, Generic, List, Optional, TypeVar
from pydantic import Field, BaseModel
from guardrails_ai.types.reask import ReAsk
from guardrails_ai.types.validation_summary import ValidationSummary


OT = TypeVar("OT", str, List, Dict)


class ValidationOutcome(BaseModel, Generic[OT]):
    """The output from a Guard execution.

    Type parameter ``OT`` is bound to ``str | List | Dict`` and reflects the
    shape of ``validated_output``.
    """

    call_id: str = Field(
        description="Foreign key to the most recent Call this resulted from.",
        alias="callId",
    )
    raw_llm_output: Optional[str] = Field(
        default=None,
        description="The raw, unchanged string content from the LLM call.",
        alias="rawLlmOutput",
    )
    validation_summaries: Optional[List[ValidationSummary]] = Field(
        default=None, alias="validationSummaries"
    )
    validated_output: Optional[OT] = Field(default=None, alias="validatedOutput")
    reask: Optional[ReAsk] = Field(
        default=None,
        description="If validation continuously fails and all allocated reasks are used, this field will contain the final reask that would have been sent to the LLM if additional reasks were available.",
    )
    validation_passed: Optional[bool] = Field(
        default=None,
        description="A boolean to indicate whether or not the LLM output passed validation.  If this is False, the validated_output may be invalid.",
        alias="validationPassed",
    )
    error: Optional[str] = Field(
        default=None,
        description="If the validation process raised a handleable exception, this field will contain the error message.",
    )

    model_config = {"validate_by_alias": True, "validate_by_name": True}
