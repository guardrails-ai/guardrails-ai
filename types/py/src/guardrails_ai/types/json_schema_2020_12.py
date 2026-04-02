"""
Strongly typed Pydantic models for JSON Schema Draft 2020-12.

Based on the specification at: https://json-schema.org/draft/2020-12/schema

This implementation supports all seven vocabularies:
- Core: $id, $schema, $ref, $defs, $anchor, $dynamicRef, $dynamicAnchor, $vocabulary, $comment
- Applicator: properties, patternProperties, additionalProperties, items, prefixItems, etc.
- Validation: type, enum, const, maximum, minimum, pattern, required, etc.
- Meta-Data: title, description, default, deprecated, readOnly, writeOnly, examples
- Format Annotation: format
- Content: contentEncoding, contentMediaType, contentSchema
- Unevaluated: unevaluatedItems, unevaluatedProperties
"""

from __future__ import annotations

from typing import Any, Dict, List, TypeAlias, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class JSONSchema(BaseModel):
    """
    A strongly typed representation of JSON Schema Draft 2020-12.

    JSON Schema can be either a boolean or an object with various properties.
    When boolean:
    - true: validates any instance
    - false: validates no instance

    When object: contains various keywords from different vocabularies.
    """

    # ========================================================================
    # CORE VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/core
    # ========================================================================

    schema_: str | None = Field(
        default=None, alias="$schema", description="URI of the meta-schema"
    )
    id: str | None = Field(
        default=None, alias="$id", description="URI identifier for the schema"
    )
    ref: str | None = Field(
        default=None, alias="$ref", description="URI reference to a schema"
    )
    anchor: str | None = Field(
        default=None,
        alias="$anchor",
        description="Plain name fragment for static referencing",
    )
    dynamic_ref: str | None = Field(
        default=None, alias="$dynamicRef", description="Dynamic URI reference"
    )
    dynamic_anchor: str | None = Field(
        default=None, alias="$dynamicAnchor", description="Dynamic anchor name"
    )
    vocabulary: Dict[str, bool] | None = Field(
        default=None,
        alias="$vocabulary",
        description="Mapping of vocabulary URIs to required (true) or optional (false)",
    )
    comment: str | None = Field(
        default=None, alias="$comment", description="Comments for schema authors"
    )
    defs: Dict[str, SchemaValue] | None = Field(
        default=None,
        alias="$defs",
        description="Container for reusable schema definitions",
    )

    # ========================================================================
    # APPLICATOR VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/applicator
    # ========================================================================

    # Object applicators
    properties: Dict[str, SchemaValue] | None = Field(
        default=None, description="Schema for object properties by name"
    )
    pattern_properties: Dict[str, SchemaValue] | None = Field(
        default=None,
        alias="patternProperties",
        description="Schema for object properties matching regex patterns",
    )
    additional_properties: SchemaValue | None = Field(
        default=None,
        alias="additionalProperties",
        description="Schema for object properties not matched by 'properties' or 'patternProperties'",
    )
    property_names: SchemaValue | None = Field(
        default=None,
        alias="propertyNames",
        description="Schema that all property names must validate against",
    )

    # Array applicators
    items: SchemaValue | None = Field(
        default=None,
        description="Schema for array items (all items, or items after prefixItems)",
    )
    prefix_items: List[SchemaValue] | None = Field(
        default=None,
        alias="prefixItems",
        description="Schemas for array items by index (tuple validation)",
    )
    contains: SchemaValue | None = Field(
        default=None,
        description="Schema that at least one array item must validate against",
    )

    # Conditional applicators
    if_: SchemaValue | None = Field(
        default=None, alias="if", description="Conditional schema"
    )
    then: SchemaValue | None = Field(
        default=None, description="Schema applied if 'if' succeeds"
    )
    else_: SchemaValue | None = Field(
        default=None, alias="else", description="Schema applied if 'if' fails"
    )

    # Composition applicators
    all_of: List[SchemaValue] | None = Field(
        default=None, alias="allOf", description="Must validate against all schemas"
    )
    any_of: List[SchemaValue] | None = Field(
        default=None,
        alias="anyOf",
        description="Must validate against at least one schema",
    )
    one_of: List[SchemaValue] | None = Field(
        default=None,
        alias="oneOf",
        description="Must validate against exactly one schema",
    )
    not_: SchemaValue | None = Field(
        default=None, alias="not", description="Must NOT validate against this schema"
    )

    # Dependent schemas
    dependent_schemas: Dict[str, SchemaValue] | None = Field(
        default=None,
        alias="dependentSchemas",
        description="Schemas applied when specific properties are present",
    )

    # ========================================================================
    # VALIDATION VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/validation
    # ========================================================================

    # Any type
    type: StringOrStringArray | None = Field(
        default=None,
        description="Type or types the instance must be (null, boolean, object, array, number, string, integer)",
    )
    enum: List[Any] | None = Field(
        default=None, description="Instance must equal one of these values"
    )
    const: Any | None = Field(
        default=None, description="Instance must equal this exact value"
    )

    # Numeric
    multiple_of: float | int | None = Field(
        default=None,
        alias="multipleOf",
        gt=0,
        description="Number must be a multiple of this value",
    )
    maximum: float | int | None = Field(
        default=None, description="Maximum numeric value (inclusive)"
    )
    exclusive_maximum: float | int | None = Field(
        default=None,
        alias="exclusiveMaximum",
        description="Maximum numeric value (exclusive)",
    )
    minimum: float | int | None = Field(
        default=None, description="Minimum numeric value (inclusive)"
    )
    exclusive_minimum: float | int | None = Field(
        default=None,
        alias="exclusiveMinimum",
        description="Minimum numeric value (exclusive)",
    )

    # String
    max_length: int | None = Field(
        default=None, alias="maxLength", ge=0, description="Maximum string length"
    )
    min_length: int | None = Field(
        default=None, alias="minLength", ge=0, description="Minimum string length"
    )
    pattern: str | None = Field(
        default=None, description="Regular expression pattern the string must match"
    )

    # Array
    max_items: int | None = Field(
        default=None, alias="maxItems", ge=0, description="Maximum array length"
    )
    min_items: int | None = Field(
        default=None, alias="minItems", ge=0, description="Minimum array length"
    )
    unique_items: bool | None = Field(
        default=None,
        alias="uniqueItems",
        description="Whether array items must be unique",
    )
    max_contains: int | None = Field(
        default=None,
        alias="maxContains",
        ge=0,
        description="Maximum number of items that must match 'contains' schema",
    )
    min_contains: int | None = Field(
        default=None,
        alias="minContains",
        ge=0,
        description="Minimum number of items that must match 'contains' schema",
    )

    # Object
    max_properties: int | None = Field(
        default=None,
        alias="maxProperties",
        ge=0,
        description="Maximum number of properties",
    )
    min_properties: int | None = Field(
        default=None,
        alias="minProperties",
        ge=0,
        description="Minimum number of properties",
    )
    required: List[str] | None = Field(
        default=None, description="Required property names"
    )
    dependent_required: Dict[str, List[str]] | None = Field(
        default=None,
        alias="dependentRequired",
        description="Required properties when specific properties are present",
    )

    # ========================================================================
    # META-DATA VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/meta-data
    # ========================================================================

    title: str | None = Field(default=None, description="Short title for the schema")
    description: str | None = Field(
        default=None, description="Explanation about the purpose of the schema"
    )
    default: Any | None = Field(default=None, description="Default value")
    deprecated: bool | None = Field(
        default=None, description="Whether the schema is deprecated"
    )
    read_only: bool | None = Field(
        default=None, alias="readOnly", description="Whether the value is read-only"
    )
    write_only: bool | None = Field(
        default=None, alias="writeOnly", description="Whether the value is write-only"
    )
    examples: List[Any] | None = Field(
        default=None, description="Example valid instances"
    )

    # ========================================================================
    # FORMAT ANNOTATION VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/format-annotation
    # https://json-schema.org/draft/2020-12/vocab/format-assertion
    # ========================================================================

    format: str | None = Field(
        default=None,
        description=(
            "Semantic format for string values. Common formats: "
            "date-time, date, time, duration, email, idn-email, hostname, idn-hostname, "
            "ipv4, ipv6, uri, uri-reference, iri, iri-reference, uuid, uri-template, "
            "json-pointer, relative-json-pointer, regex"
        ),
    )

    # ========================================================================
    # CONTENT VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/content
    # ========================================================================

    content_encoding: str | None = Field(
        default=None,
        alias="contentEncoding",
        description="Encoding used for string content (e.g., base64, quoted-printable)",
    )
    content_media_type: str | None = Field(
        default=None,
        alias="contentMediaType",
        description="Media type of string content (e.g., application/json, text/html)",
    )
    content_schema: SchemaValue | None = Field(
        default=None,
        alias="contentSchema",
        description="Schema for the decoded string content",
    )

    # ========================================================================
    # UNEVALUATED VOCABULARY
    # https://json-schema.org/draft/2020-12/vocab/unevaluated
    # ========================================================================

    unevaluated_items: SchemaValue | None = Field(
        default=None,
        alias="unevaluatedItems",
        description="Schema for array items not evaluated by other keywords",
    )
    unevaluated_properties: SchemaValue | None = Field(
        default=None,
        alias="unevaluatedProperties",
        description="Schema for object properties not evaluated by other keywords",
    )

    # ========================================================================
    # DEPRECATED KEYWORDS (for backward compatibility)
    # https://json-schema.org/draft/2020-12/release-notes
    # ========================================================================

    definitions: Dict[str, SchemaValue] | None = Field(
        default=None,
        description="DEPRECATED: Use $defs instead. Container for reusable schema definitions.",
    )
    dependencies: Dict[str, Union[SchemaValue, List[str]]] | None = Field(
        default=None,
        description="DEPRECATED: Use dependentSchemas and dependentRequired instead.",
    )
    recursive_anchor: bool | None = Field(
        default=None,
        alias="$recursiveAnchor",
        description="DEPRECATED: Use $dynamicAnchor instead.",
    )
    recursive_ref: str | None = Field(
        default=None,
        alias="$recursiveRef",
        description="DEPRECATED: Use $dynamicRef instead.",
    )

    model_config = {
        "extra": "allow",  # Allow additional properties for extensibility
        "validate_by_alias": True,
        "validate_by_name": True,
    }

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: StringOrStringArray | None) -> StringOrStringArray | None:
        """Validate that type values are one of the allowed JSON Schema types."""
        if v is None:
            return v

        allowed_types = {
            "null",
            "boolean",
            "object",
            "array",
            "number",
            "string",
            "integer",
        }

        if isinstance(v, str):
            if v not in allowed_types:
                raise ValueError(f"Invalid type: {v}. Must be one of {allowed_types}")
        elif isinstance(v, list):
            for t in v:
                if not isinstance(t, str):
                    raise ValueError(
                        f"Type array must contain only strings, got {type(t)}"
                    )
                if t not in allowed_types:
                    raise ValueError(
                        f"Invalid type: {t}. Must be one of {allowed_types}"
                    )
            # Check for duplicates
            if len(v) != len(set(v)):
                raise ValueError("Type array must not contain duplicates")

        return v

    @model_validator(mode="after")
    def validate_contains_constraints(self) -> "JSONSchema":
        """Validate that minContains and maxContains are used with contains."""
        if (
            self.min_contains is not None or self.max_contains is not None
        ) and self.contains is None:
            raise ValueError(
                "minContains and maxContains can only be used with contains"
            )

        if self.min_contains is not None and self.max_contains is not None:
            if self.min_contains > self.max_contains:
                raise ValueError(
                    "minContains must be less than or equal to maxContains"
                )

        return self

    @model_validator(mode="after")
    def validate_length_constraints(self) -> "JSONSchema":
        """Validate min/max length constraints."""
        if self.min_length is not None and self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError("minLength must be less than or equal to maxLength")

        if self.min_items is not None and self.max_items is not None:
            if self.min_items > self.max_items:
                raise ValueError("minItems must be less than or equal to maxItems")

        if self.min_properties is not None and self.max_properties is not None:
            if self.min_properties > self.max_properties:
                raise ValueError(
                    "minProperties must be less than or equal to maxProperties"
                )

        return self

    @model_validator(mode="after")
    def validate_numeric_constraints(self) -> "JSONSchema":
        """Validate numeric constraints."""
        if self.minimum is not None and self.maximum is not None:
            if self.minimum > self.maximum:
                raise ValueError("minimum must be less than or equal to maximum")

        if self.exclusive_minimum is not None and self.exclusive_maximum is not None:
            if self.exclusive_minimum >= self.exclusive_maximum:
                raise ValueError("exclusiveMinimum must be less than exclusiveMaximum")

        return self

    @model_validator(mode="after")
    def validate_conditional(self) -> "JSONSchema":
        """Validate that then/else are only used with if."""
        if (self.then is not None or self.else_ is not None) and self.if_ is None:
            raise ValueError("'then' and 'else' can only be used with 'if'")

        return self


# Type aliases for clarity
Schema: TypeAlias = Union[bool, JSONSchema]
SchemaValue: TypeAlias = Union[bool, JSONSchema]
StringOrStringArray: TypeAlias = Union[str, List[str]]


def create_schema(**kwargs: Any) -> JSONSchema:
    """
    Convenience function to create a JSONSchema instance.

    Args:
        **kwargs: Keyword arguments corresponding to JSONSchema fields.
                  Use the Pythonic field names (e.g., 'schema' instead of '$schema').

    Returns:
        A JSONSchema instance.

    Example:
        >>> schema = create_schema(
        ...     type="object",
        ...     properties={
        ...         "name": {"type": "string"},
        ...         "age": {"type": "integer", "minimum": 0}
        ...     },
        ...     required=["name"]
        ... )
    """
    return JSONSchema(**kwargs)


def create_boolean_schema(value: bool) -> bool:
    """
    Create a boolean schema.

    Args:
        value: True to validate all instances, False to validate no instances.

    Returns:
        The boolean value.

    Example:
        >>> always_valid = create_boolean_schema(True)
        >>> never_valid = create_boolean_schema(False)
    """
    return value


# Common schema patterns as helper functions


def string_schema(
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | None = None,
    format: str | None = None,
    **kwargs: Any,
) -> JSONSchema:
    """Create a string schema with common constraints."""
    return JSONSchema(
        type="string",
        minLength=min_length,
        maxLength=max_length,
        pattern=pattern,
        format=format,
        **kwargs,
    )


def number_schema(
    minimum: float | int | None = None,
    maximum: float | int | None = None,
    exclusive_minimum: float | int | None = None,
    exclusive_maximum: float | int | None = None,
    multiple_of: float | int | None = None,
    is_integer: bool = False,
    **kwargs: Any,
) -> JSONSchema:
    """Create a number or integer schema with common constraints."""
    return JSONSchema(
        type="integer" if is_integer else "number",
        minimum=minimum,
        maximum=maximum,
        exclusiveMinimum=exclusive_minimum,
        exclusiveMaximum=exclusive_maximum,
        multipleOf=multiple_of,
        **kwargs,
    )


def array_schema(
    items: SchemaValue | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    unique_items: bool | None = None,
    **kwargs: Any,
) -> JSONSchema:
    """Create an array schema with common constraints."""
    return JSONSchema(
        type="array",
        items=items,
        minItems=min_items,
        maxItems=max_items,
        uniqueItems=unique_items,
        **kwargs,
    )


def object_schema(
    properties: Dict[str, SchemaValue] | None = None,
    required: List[str] | None = None,
    additional_properties: SchemaValue | None = None,
    min_properties: int | None = None,
    max_properties: int | None = None,
    **kwargs: Any,
) -> JSONSchema:
    """Create an object schema with common constraints."""
    return JSONSchema(
        type="object",
        properties=properties,
        required=required,
        additionalProperties=additional_properties,
        minProperties=min_properties,
        maxProperties=max_properties,
        **kwargs,
    )


def enum_schema(values: List[Any], **kwargs: Any) -> JSONSchema:
    """Create an enum schema."""
    return JSONSchema(enum=values, **kwargs)


def const_schema(value: Any, **kwargs: Any) -> JSONSchema:
    """Create a const schema."""
    return JSONSchema(const=value, **kwargs)


def ref_schema(ref: str, **kwargs: Any) -> JSONSchema:
    """Create a reference schema."""
    return JSONSchema(ref=ref, **kwargs)  # type: ignore PEP 681 issue


def all_of_schema(*schemas: "SchemaValue", **kwargs: Any) -> JSONSchema:
    """Create an allOf composition schema."""
    return JSONSchema(all_of=list(schemas), **kwargs)  # type: ignore PEP 681 issue


def any_of_schema(*schemas: "SchemaValue", **kwargs: Any) -> JSONSchema:
    """Create an anyOf composition schema."""
    return JSONSchema(any_of=list(schemas), **kwargs)  # type: ignore PEP 681 issue


def one_of_schema(*schemas: "SchemaValue", **kwargs: Any) -> JSONSchema:
    """Create a oneOf composition schema."""
    return JSONSchema(one_of=list(schemas), **kwargs)  # type: ignore PEP 681 issue


def not_schema(schema: "SchemaValue", **kwargs: Any) -> JSONSchema:
    """Create a not schema."""
    return JSONSchema(not_=schema, **kwargs)  # type: ignore PEP 681 issue
