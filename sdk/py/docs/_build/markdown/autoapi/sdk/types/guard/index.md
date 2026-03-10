# sdk.types.guard

## Classes

| [`Guard`](#sdk.types.guard.Guard)   | A configured validation pipeline retrieved from the Guardrails API.   |
|-------------------------------------|-----------------------------------------------------------------------|

## Module Contents

### *class* sdk.types.guard.Guard(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

A configured validation pipeline retrieved from the Guardrails API.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### description *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### output_schema *: guardrails_ai.sdk.types.json_schema_2020_12.JSONSchema* *= None*

#### validators *: List[guardrails_ai.sdk.types.validator.Validator]* *= None*
