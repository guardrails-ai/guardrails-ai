# types.error_span

## Classes

| [`ErrorSpan`](#types.error_span.ErrorSpan)   | Character-level span within validated text that caused a validation failure.   |
|----------------------------------------------|--------------------------------------------------------------------------------|

## Module Contents

### *class* types.error_span.ErrorSpan(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

Character-level span within validated text that caused a validation failure.

Useful for pinpointing failures when validating large chunks of text or
streaming output with varying chunk sizes.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### end *: [int](https://docs.python.org/3/library/functions.html#int)*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### reason *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### start *: [int](https://docs.python.org/3/library/functions.html#int)*
