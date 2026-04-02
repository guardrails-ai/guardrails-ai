from __future__ import annotations
from pydantic import BaseModel, Field


class ErrorSpan(BaseModel):
    """Character-level span within validated text that caused a validation failure.

    Useful for pinpointing failures when validating large chunks of text or
    streaming output with varying chunk sizes.
    """

    start: int = Field(description="Starting index relative to the validated chunk.")
    end: int = Field(description="Ending index relative to the validated chunk.")
    reason: str = Field(
        description="The reason validation failed, specific to this chunk."
    )

    model_config = {"validate_by_alias": True, "validate_by_name": True}
