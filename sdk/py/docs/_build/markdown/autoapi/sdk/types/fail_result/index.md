# sdk.types.fail_result

## Classes

| [`FailResult`](#sdk.types.fail_result.FailResult)   | The output of a validator when validation fails.   |
|-----------------------------------------------------|----------------------------------------------------|

## Module Contents

### *class* sdk.types.fail_result.FailResult(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

The output of a validator when validation fails.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### error_message *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### error_spans *: List[guardrails_ai.sdk.types.error_span.ErrorSpan] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### fix_value *: Any | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### metadata *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), Any] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### outcome *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

#### validated_chunk *: Any | [None](https://docs.python.org/3/library/constants.html#None)* *= None*
