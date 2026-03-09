from __future__ import annotations
from pydantic import BaseModel, Field


class ErrorSpan(BaseModel):
    """
    ErrorSpan provide additional context for why a validation failed. They
    specify the start and end index of the segment that caused the failure,
    which can be useful when validating large chunks of text or validating
    while streaming with different chunking methods.
    """

    start: int
    end: int
    reason: str = Field(
        description="The reason validation failed, specific to this chunk."
    )

    model_config = {"validate_by_alias": True, "validate_by_name": True}
