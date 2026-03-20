from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from guardrails_ai.types.json_schema_2020_12 import JSONSchema, string_schema
from guardrails_ai.types.validator import Validator


class CreateGuardRequest(BaseModel):
    """The required request body to created a Guard in the Guardrails API."""

    name: str = Field(description="The name for the Guard.")
    description: Optional[str] = Field(
        default=None,
        description="A description that concisely states the expected behaviour or purpose of the Guard.",
    )
    validators: List[Validator] = Field(default_factory=list)
    output_schema: JSONSchema = Field(default_factory=string_schema)

    model_config = {"validate_by_alias": True, "validate_by_name": True}


class Guard(CreateGuardRequest):
    """A configured validation pipeline retrieved from the Guardrails API."""

    id: str = Field(description="The unique identifier for the Guard.")

    model_config = {"validate_by_alias": True, "validate_by_name": True}
