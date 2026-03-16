# types.json_schema_2020_12

Strongly typed Pydantic models for JSON Schema Draft 2020-12.

Based on the specification at: [https://json-schema.org/draft/2020-12/schema](https://json-schema.org/draft/2020-12/schema)

This implementation supports all seven vocabularies:
- Core: $id, $schema, $ref, $defs, $anchor, $dynamicRef, $dynamicAnchor, $vocabulary, $comment
- Applicator: properties, patternProperties, additionalProperties, items, prefixItems, etc.
- Validation: type, enum, const, maximum, minimum, pattern, required, etc.
- Meta-Data: title, description, default, deprecated, readOnly, writeOnly, examples
- Format Annotation: format
- Content: contentEncoding, contentMediaType, contentSchema
- Unevaluated: unevaluatedItems, unevaluatedProperties

## Attributes

| [`Schema`](#types.json_schema_2020_12.Schema)                           |    |
|-------------------------------------------------------------------------|----|
| [`SchemaValue`](#types.json_schema_2020_12.SchemaValue)                 |    |
| [`StringOrStringArray`](#types.json_schema_2020_12.StringOrStringArray) |    |

## Classes

| [`JSONSchema`](#types.json_schema_2020_12.JSONSchema)   | A strongly typed representation of JSON Schema Draft 2020-12.   |
|---------------------------------------------------------|-----------------------------------------------------------------|

## Functions

| [`all_of_schema`](#types.json_schema_2020_12.all_of_schema)(→ JSONSchema)           | Create an allOf composition schema.                        |
|-------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`any_of_schema`](#types.json_schema_2020_12.any_of_schema)(→ JSONSchema)           | Create an anyOf composition schema.                        |
| [`array_schema`](#types.json_schema_2020_12.array_schema)(→ JSONSchema)             | Create an array schema with common constraints.            |
| [`const_schema`](#types.json_schema_2020_12.const_schema)(→ JSONSchema)             | Create a const schema.                                     |
| [`create_boolean_schema`](#types.json_schema_2020_12.create_boolean_schema)(→ bool) | Create a boolean schema.                                   |
| [`create_schema`](#types.json_schema_2020_12.create_schema)(→ JSONSchema)           | Convenience function to create a JSONSchema instance.      |
| [`enum_schema`](#types.json_schema_2020_12.enum_schema)(→ JSONSchema)               | Create an enum schema.                                     |
| [`not_schema`](#types.json_schema_2020_12.not_schema)(→ JSONSchema)                 | Create a not schema.                                       |
| [`number_schema`](#types.json_schema_2020_12.number_schema)(→ JSONSchema)           | Create a number or integer schema with common constraints. |
| [`object_schema`](#types.json_schema_2020_12.object_schema)(→ JSONSchema)           | Create an object schema with common constraints.           |
| [`one_of_schema`](#types.json_schema_2020_12.one_of_schema)(→ JSONSchema)           | Create a oneOf composition schema.                         |
| [`ref_schema`](#types.json_schema_2020_12.ref_schema)(→ JSONSchema)                 | Create a reference schema.                                 |
| [`string_schema`](#types.json_schema_2020_12.string_schema)(→ JSONSchema)           | Create a string schema with common constraints.            |

## Module Contents

### *class* types.json_schema_2020_12.JSONSchema(/, \*\*data: Any)

Bases: [`pydantic.BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel)

A strongly typed representation of JSON Schema Draft 2020-12.

JSON Schema can be either a boolean or an object with various properties.
When boolean:
- true: validates any instance
- false: validates no instance

When object: contains various keywords from different vocabularies.

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### validate_conditional() → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Validate that then/else are only used with if.

#### validate_contains_constraints() → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Validate that minContains and maxContains are used with contains.

#### validate_length_constraints() → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Validate min/max length constraints.

#### validate_numeric_constraints() → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Validate numeric constraints.

#### *classmethod* validate_type(v: [StringOrStringArray](#types.json_schema_2020_12.StringOrStringArray) | [None](https://docs.python.org/3/library/constants.html#None)) → [StringOrStringArray](#types.json_schema_2020_12.StringOrStringArray) | [None](https://docs.python.org/3/library/constants.html#None)

Validate that type values are one of the allowed JSON Schema types.

#### additional_properties *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### all_of *: List[[SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### anchor *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### any_of *: List[[SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### comment *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### const *: Any | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### contains *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### content_encoding *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### content_media_type *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### content_schema *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### default *: Any | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### definitions *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### defs *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### dependencies *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue) | List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### dependent_required *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### dependent_schemas *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### deprecated *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### description *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### dynamic_anchor *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### dynamic_ref *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### else_ *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### enum *: List[Any] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### examples *: List[Any] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### exclusive_maximum *: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### exclusive_minimum *: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### format *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### if_ *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### items *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### max_contains *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### max_items *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### max_length *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### max_properties *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### maximum *: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### min_contains *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### min_items *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### min_length *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### min_properties *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### minimum *: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### model_config

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### multiple_of *: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### not_ *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### one_of *: List[[SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### pattern *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### pattern_properties *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### prefix_items *: List[[SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### properties *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### property_names *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### read_only *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### recursive_anchor *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### recursive_ref *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### ref *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### required *: List[[str](https://docs.python.org/3/library/stdtypes.html#str)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### schema_ *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### then *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### title *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### type *: [StringOrStringArray](#types.json_schema_2020_12.StringOrStringArray) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### unevaluated_items *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### unevaluated_properties *: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### unique_items *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### vocabulary *: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [bool](https://docs.python.org/3/library/functions.html#bool)] | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

#### write_only *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

### types.json_schema_2020_12.all_of_schema(\*schemas: [SchemaValue](#types.json_schema_2020_12.SchemaValue), \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create an allOf composition schema.

### types.json_schema_2020_12.any_of_schema(\*schemas: [SchemaValue](#types.json_schema_2020_12.SchemaValue), \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create an anyOf composition schema.

### types.json_schema_2020_12.array_schema(items: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None) = None, min_items: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, max_items: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, unique_items: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None) = None, \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create an array schema with common constraints.

### types.json_schema_2020_12.const_schema(value: Any, \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create a const schema.

### types.json_schema_2020_12.create_boolean_schema(value: [bool](https://docs.python.org/3/library/functions.html#bool)) → [bool](https://docs.python.org/3/library/functions.html#bool)

Create a boolean schema.

* **Parameters:**
  **value** – True to validate all instances, False to validate no instances.
* **Returns:**
  The boolean value.

### Example

```pycon
>>> always_valid = create_boolean_schema(True)
>>> never_valid = create_boolean_schema(False)
```

### types.json_schema_2020_12.create_schema(\*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Convenience function to create a JSONSchema instance.

* **Parameters:**
  **\*\*kwargs** – Keyword arguments corresponding to JSONSchema fields.
  Use the Pythonic field names (e.g., ‘

  ```
  schema_
  ```

  ’ instead of ‘$schema’).
* **Returns:**
  A JSONSchema instance.

### Example

```pycon
>>> schema = create_schema(
...     type="object",
...     properties={
...         "name": {"type": "string"},
...         "age": {"type": "integer", "minimum": 0}
...     },
...     required=["name"]
... )
```

### types.json_schema_2020_12.enum_schema(values: List[Any], \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create an enum schema.

### types.json_schema_2020_12.not_schema(schema: [SchemaValue](#types.json_schema_2020_12.SchemaValue), \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create a not schema.

### types.json_schema_2020_12.number_schema(minimum: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, maximum: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, exclusive_minimum: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, exclusive_maximum: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, multiple_of: [float](https://docs.python.org/3/library/functions.html#float) | [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, is_integer: [bool](https://docs.python.org/3/library/functions.html#bool) = False, \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create a number or integer schema with common constraints.

### types.json_schema_2020_12.object_schema(properties: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), [SchemaValue](#types.json_schema_2020_12.SchemaValue)] | [None](https://docs.python.org/3/library/constants.html#None) = None, required: List[[str](https://docs.python.org/3/library/stdtypes.html#str)] | [None](https://docs.python.org/3/library/constants.html#None) = None, additional_properties: [SchemaValue](#types.json_schema_2020_12.SchemaValue) | [None](https://docs.python.org/3/library/constants.html#None) = None, min_properties: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, max_properties: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create an object schema with common constraints.

### types.json_schema_2020_12.one_of_schema(\*schemas: [SchemaValue](#types.json_schema_2020_12.SchemaValue), \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create a oneOf composition schema.

### types.json_schema_2020_12.ref_schema(ref: [str](https://docs.python.org/3/library/stdtypes.html#str), \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create a reference schema.

### types.json_schema_2020_12.string_schema(min_length: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, max_length: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None) = None, pattern: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None) = None, format: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None) = None, \*\*kwargs: Any) → [JSONSchema](#types.json_schema_2020_12.JSONSchema)

Create a string schema with common constraints.

### types.json_schema_2020_12.Schema

### types.json_schema_2020_12.SchemaValue

### types.json_schema_2020_12.StringOrStringArray
