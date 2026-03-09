# sdk.types.validation_outcome

## Attributes

| [`OT`](#sdk.types.validation_outcome.OT)   |    |
|--------------------------------------------|----|

## Classes

| [`ValidationOutcome`](#sdk.types.validation_outcome.ValidationOutcome)   | The output from a Guard execution.   |
|--------------------------------------------------------------------------|--------------------------------------|

## Module Contents

### *class* sdk.types.validation_outcome.ValidationOutcome(/, \*\*data: Any)

Bases: `Generic`[[`OT`](#sdk.types.validation_outcome.OT)], [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

The output from a Guard execution.

Type parameter `OT` is bound to `str | List | Dict` and reflects the
shape of `validated_output`.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### call_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### error *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### raw_llm_output *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### reask *: guardrails_ai.sdk.types.reask.ReAsk | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### validated_output *: [OT](#sdk.types.validation_outcome.OT) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### validation_passed *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### validation_summaries *: List[guardrails_ai.sdk.types.validation_summary.ValidationSummary] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

### sdk.types.validation_outcome.OT
