# sdk.types.on_fail

## Classes

| [`OnFail`](#sdk.types.on_fail.OnFail)   | OnFail is an Enum that represents the different actions that can   |
|-----------------------------------------|--------------------------------------------------------------------|

## Module Contents

### *class* sdk.types.on_fail.OnFail

Bases: [`str`](https://docs.python.org/3/library/stdtypes.html#str), [`enum.Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

OnFail is an Enum that represents the different actions that can
be taken when a validation fails.

#### REASK

On failure, Reask the LLM.

* **Type:**
  Literal[“reask”]

#### FIX

On failure, apply a static fix.

* **Type:**
  Literal[“fix”]

#### FILTER

On failure, filter out the invalid values.

* **Type:**
  Literal[“filter”]

#### REFRAIN

On failure, refrain from responding;
return an empty value.

* **Type:**
  Literal[“refrain”]

#### NOOP

On failure, do nothing.

* **Type:**
  Literal[“noop”]

#### EXCEPTION

On failure, raise a ValidationError.

* **Type:**
  Literal[“exception”]

#### FIX_REASK

On failure, apply a static fix,
check if the fixed value passed validation, if not then reask the LLM.

* **Type:**
  Literal[“fix_reask”]

#### CUSTOM

On failure, call a custom function with the
invalid value and the FailResult’s from any validators run on the value.

* **Type:**
  Literal[“custom”]

Initialize self.  See help(type(self)) for accurate signature.

#### CUSTOM *= 'custom'*

#### EXCEPTION *= 'exception'*

#### FILTER *= 'filter'*

#### FIX *= 'fix'*

#### FIX_REASK *= 'fix_reask'*

#### NOOP *= 'noop'*

#### REASK *= 'reask'*

#### REFRAIN *= 'refrain'*
