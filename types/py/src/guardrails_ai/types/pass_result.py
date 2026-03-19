from typing import Any, Literal, Optional
from pydantic import Field, field_serializer, field_validator

from guardrails_ai.types.validation_result import ValidationResult, Outcome


class PassResult(ValidationResult):
    """
    PassResult is the output type of Validator.validate when validation
    succeeds.
    """

    class ValueOverrideSentinel:
        pass

    # should only be used if Validator.override_value_on_pass is True
    value_override: Optional[Any] = Field(
        default=ValueOverrideSentinel,
        description="The value to use as an override if validation passes.",
    )

    @field_serializer("value_override", when_used="json")
    def serialize_value_override(self, value_override: Any | None) -> Any | None:
        if value_override is not self.ValueOverrideSentinel:
            return value_override
        return None

    @field_validator("outcome")
    @classmethod
    def deserialize_outcome(cls, outcome: str | None) -> Literal[Outcome.PASS]:
        return Outcome.PASS
