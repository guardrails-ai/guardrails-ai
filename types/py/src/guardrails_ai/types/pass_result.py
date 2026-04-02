from typing import Any, Literal, Optional
from pydantic import Field, field_serializer, field_validator

from guardrails_ai.types.validation_result import ValidationResult, Outcome


class PassResult(ValidationResult):
    """
    PassResult is the output type of Validator.validate when validation
    succeeds.
    """

    outcome: Outcome = Outcome.PASS

    class ValueOverrideSentinel:
        pass

    # should only be used if Validator.override_value_on_pass is True
    value_override: Optional[Any] = Field(
        default=ValueOverrideSentinel,
        description="The value to use as an override if validation passes.",
    )

    @field_serializer("value_override")
    def serialize_value_override(self, value_override: Any | None) -> Any | None:
        if value_override is not self.ValueOverrideSentinel:
            return value_override
        return None

    @field_validator("value_override")
    @classmethod
    def deserialize_value_override(
        cls, value_override: Any | None
    ) -> ValueOverrideSentinel | Any | None:
        if value_override is None:
            return cls.ValueOverrideSentinel
        return value_override

    @field_validator("outcome")
    @classmethod
    def deserialize_outcome(cls, outcome: str | None) -> Literal[Outcome.PASS]:
        return Outcome.PASS
