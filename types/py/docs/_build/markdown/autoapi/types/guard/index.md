# types.guard

## Classes

| [`CreateGuardRequest`](#types.guard.CreateGuardRequest)   | The required request body to created a Guard in the Guardrails API.   |
|-----------------------------------------------------------|-----------------------------------------------------------------------|
| [`Guard`](#types.guard.Guard)                             | A configured validation pipeline retrieved from the Guardrails API.   |

## Module Contents

### *class* types.guard.CreateGuardRequest(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

The required request body to created a Guard in the Guardrails API.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### description *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### output_schema *: guardrails_ai.types.json_schema_2020_12.JSONSchema* *= None*

#### validators *: List[guardrails_ai.types.validator.Validator]* *= None*

### *class* types.guard.Guard(/, \*\*data: Any)

Bases: [`CreateGuardRequest`](#types.guard.CreateGuardRequest)

A configured validation pipeline retrieved from the Guardrails API.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].
