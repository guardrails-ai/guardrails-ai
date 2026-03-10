# sdk.types.reask

## Classes

| [`ReAsk`](#sdk.types.reask.ReAsk)   | Represents a pending reask when validation fails and retries are exhausted.   |
|-------------------------------------|-------------------------------------------------------------------------------|

## Module Contents

### *class* sdk.types.reask.ReAsk(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

Represents a pending reask when validation fails and retries are exhausted.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### fail_results *: List[guardrails_ai.sdk.types.fail_result.FailResult] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### incorrect_value *: Any | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].
