# types.validation_summary

## Classes

| [`ValidationSummary`](#types.validation_summary.ValidationSummary)   | Per-validator result produced during a Guard execution.   |
|----------------------------------------------------------------------|-----------------------------------------------------------|

## Module Contents

### *class* types.validation_summary.ValidationSummary(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

Per-validator result produced during a Guard execution.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### error_spans *: List[guardrails_ai.types.error_span.ErrorSpan] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### failure_reason *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### property_path *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### validator_name *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### validator_status *: Literal['pass'] | Literal['fail']* *= None*
