from enum import Enum
from typing import Any, Dict, Optional
from pydantic import Field, BaseModel


class Outcome(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class ValidationResult(BaseModel):
    """ValidationResult is the output type of Validator.validate and the
    abstract base class for all validation results.

    """

    outcome: Outcome = Field(
        description="The outcome of the validation. Must be one of 'pass' or 'fail'."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="The metadata associated with this validation result."
    )
    validated_chunk: Optional[Any] = Field(
        default=None,
        alias="validatedChunk",
        description="The value argument passed to validator.validate or validator.validate_stream.",
    )

    model_config = {
        "validate_by_alias": True,
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
    }
