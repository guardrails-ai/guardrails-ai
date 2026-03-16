# types.validator

## Classes

| [`Validator`](#types.validator.Validator)   | A validator attached to a Guard, including its configuration.   |
|---------------------------------------------|-----------------------------------------------------------------|

## Module Contents

### *class* types.validator.Validator(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

A validator attached to a Guard, including its configuration.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### args *: List[Any] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= None*

#### kwargs *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### on *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### on_fail *: guardrails_ai.types.on_fail.OnFail | [None](https://docs.python.org/3/library/constants.html#None)* *= None*
