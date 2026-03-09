from __future__ import annotations
from pydantic import BaseModel, Field


class ErrorSpan(BaseModel):
    """Character-level span within validated text that caused a validation failure.

    Useful for pinpointing failures when validating large chunks of text or
    streaming output with varying chunk sizes.
    """

    start: int
    end: int
    reason: str = Field(
        description="The reason validation failed, specific to this chunk."
    )

    model_config = {"validate_by_alias": True, "validate_by_name": True}
