"""
Test and example usage of JSON Schema Draft 2020-12 Pydantic models.
"""

import json

import pytest
from pydantic import ValidationError

from guardrails_ai.sdk.types.json_schema_2020_12 import (
    JSONSchema,
    all_of_schema,
    any_of_schema,
    array_schema,
    const_schema,
    create_boolean_schema,
    enum_schema,
    not_schema,
    number_schema,
    object_schema,
    one_of_schema,
    ref_schema,
    string_schema,
)


class TestBasicSchemas:
    """Test basic schema creation and validation."""

    def test_boolean_schemas(self):
        """Test boolean schemas (true validates all, false validates none)."""
        always_valid = create_boolean_schema(True)
        never_valid = create_boolean_schema(False)

        assert always_valid is True
        assert never_valid is False

    def test_empty_schema(self):
        """Test empty schema (equivalent to true)."""
        schema = JSONSchema()
        assert schema.model_dump(exclude_none=True, by_alias=True) == {}

    def test_string_schema(self):
        """Test string schema with various constraints."""
        schema = string_schema(
            min_length=1,
            max_length=100,
            pattern=r"^[a-zA-Z]+$",
            format="email",
            title="Email Address",
            description="User's email address",
        )

        assert schema.type == "string"
        assert schema.min_length == 1
        assert schema.max_length == 100
        assert schema.pattern == r"^[a-zA-Z]+$"
        assert schema.format == "email"

    def test_number_schema(self):
        """Test number and integer schemas."""
        int_schema = number_schema(
            minimum=0, maximum=100, multiple_of=5, is_integer=True
        )

        assert int_schema.type == "integer"
        assert int_schema.minimum == 0
        assert int_schema.maximum == 100
        assert int_schema.multiple_of == 5

        float_schema = number_schema(exclusive_minimum=0.0, exclusive_maximum=1.0)

        assert float_schema.type == "number"
        assert float_schema.exclusive_minimum == 0.0
        assert float_schema.exclusive_maximum == 1.0

    def test_array_schema(self):
        """Test array schema with item constraints."""
        schema = array_schema(
            items={"type": "string"}, min_items=1, max_items=10, unique_items=True
        )

        assert schema.type == "array"
        assert schema.items == {"type": "string"}
        assert schema.min_items == 1
        assert schema.max_items == 10
        assert schema.unique_items is True

    def test_object_schema(self):
        """Test object schema with properties and constraints."""
        schema = object_schema(
            properties={
                "name": string_schema(min_length=1),
                "age": number_schema(minimum=0, is_integer=True),
                "email": string_schema(format="email"),
            },
            required=["name", "email"],
            additional_properties=False,
        )

        assert schema.type == "object"
        assert "name" in schema.properties
        assert "age" in schema.properties
        assert "email" in schema.properties
        assert schema.required == ["name", "email"]
        assert schema.additional_properties is False


class TestValidation:
    """Test validation of schema constraints."""

    def test_type_validation(self):
        """Test type field validation."""
        # Valid single type
        schema = JSONSchema(type="string")
        assert schema.type == "string"

        # Valid array of types
        schema = JSONSchema(type=["string", "number"])
        assert schema.type == ["string", "number"]

        # Invalid type
        with pytest.raises(ValidationError):
            JSONSchema(type="invalid")

        # Invalid type in array
        with pytest.raises(ValidationError):
            JSONSchema(type=["string", "invalid"])

        # Duplicate types
        with pytest.raises(ValidationError):
            JSONSchema(type=["string", "string"])

    def test_length_constraints(self):
        """Test min/max length validation."""
        # Valid
        schema = JSONSchema(min_length=1, max_length=10)
        assert schema.min_length == 1

        # Invalid: min > max
        with pytest.raises(ValidationError):
            JSONSchema(min_length=10, max_length=1)

    def test_items_constraints(self):
        """Test min/max items validation."""
        # Valid
        schema = JSONSchema(min_items=1, max_items=10)
        assert schema.min_items == 1

        # Invalid: min > max
        with pytest.raises(ValidationError):
            JSONSchema(min_items=10, max_items=1)

    def test_properties_constraints(self):
        """Test min/max properties validation."""
        # Valid
        schema = JSONSchema(min_properties=1, max_properties=10)
        assert schema.min_properties == 1

        # Invalid: min > max
        with pytest.raises(ValidationError):
            JSONSchema(min_properties=10, max_properties=1)

    def test_numeric_constraints(self):
        """Test numeric constraint validation."""
        # Valid
        schema = JSONSchema(minimum=0, maximum=100)
        assert schema.minimum == 0

        # Invalid: min > max
        with pytest.raises(ValidationError):
            JSONSchema(minimum=100, maximum=0)

        # Valid exclusive
        schema = JSONSchema(exclusive_minimum=0, exclusive_maximum=100)
        assert schema.exclusive_minimum == 0

        # Invalid exclusive: min >= max
        with pytest.raises(ValidationError):
            JSONSchema(exclusive_minimum=100, exclusive_maximum=100)

    def test_contains_constraints(self):
        """Test contains with minContains and maxContains."""
        # Valid
        schema = JSONSchema(contains={"type": "string"}, min_contains=1, max_contains=5)
        assert schema.min_contains == 1

        # Invalid: minContains without contains
        with pytest.raises(ValidationError):
            JSONSchema(min_contains=1)

        # Invalid: minContains > maxContains
        with pytest.raises(ValidationError):
            JSONSchema(contains={"type": "string"}, min_contains=5, max_contains=1)

    def test_conditional_constraints(self):
        """Test if/then/else validation."""
        # Valid
        schema = JSONSchema(
            if_={"type": "string"}, then={"minLength": 5}, else_={"minLength": 10}
        )
        assert schema.if_ is not None

        # Invalid: then without if
        with pytest.raises(ValidationError):
            JSONSchema(then={"minLength": 5})


class TestCoreVocabulary:
    """Test core vocabulary keywords."""

    def test_schema_and_id(self):
        """Test $schema and $id keywords."""
        schema = JSONSchema(
            schema_="https://json-schema.org/draft/2020-12/schema",
            id="https://example.com/schemas/person.json",
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert data["$id"] == "https://example.com/schemas/person.json"

    def test_ref(self):
        """Test $ref keyword."""
        schema = ref_schema("#/$defs/address")

        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert data["$ref"] == "#/$defs/address"

    def test_defs(self):
        """Test $defs keyword."""
        schema = JSONSchema(
            type="object",
            properties={"address": {"$ref": "#/$defs/address"}},
            defs={
                "address": object_schema(
                    properties={"street": string_schema(), "city": string_schema()}
                )
            },
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert "$defs" in data
        assert "address" in data["$defs"]

    def test_anchor_and_dynamic_anchor(self):
        """Test $anchor and $dynamicAnchor keywords."""
        schema = JSONSchema(
            anchor="myAnchor", dynamic_anchor="dynamicAnchor", type="string"
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert data["$anchor"] == "myAnchor"
        assert data["$dynamicAnchor"] == "dynamicAnchor"

    def test_comment(self):
        """Test $comment keyword."""
        schema = JSONSchema(
            comment="This is a comment for schema authors", type="string"
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert data["$comment"] == "This is a comment for schema authors"

    def test_vocabulary(self):
        """Test $vocabulary keyword."""
        schema = JSONSchema(
            vocabulary={
                "https://json-schema.org/draft/2020-12/vocab/core": True,
                "https://json-schema.org/draft/2020-12/vocab/applicator": True,
                "https://json-schema.org/draft/2020-12/vocab/validation": True,
                "https://example.com/custom-vocab": False,
            }
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert "$vocabulary" in data
        assert len(data["$vocabulary"]) == 4


class TestApplicatorVocabulary:
    """Test applicator vocabulary keywords."""

    def test_properties_and_pattern_properties(self):
        """Test properties and patternProperties."""
        schema = object_schema(
            properties={"name": string_schema(), "age": number_schema(is_integer=True)},
            pattern_properties={
                r"^S_": string_schema(),
                r"^I_": number_schema(is_integer=True),
            },
        )

        assert "name" in schema.properties
        assert len(schema.pattern_properties) == 2

    def test_prefix_items(self):
        """Test prefixItems for tuple validation."""
        schema = JSONSchema(
            type="array",
            prefix_items=[
                string_schema(),
                number_schema(is_integer=True),
                {"type": "boolean"},
            ],
            items=False,  # No additional items allowed
        )

        assert len(schema.prefix_items) == 3
        assert schema.items is False

    def test_contains(self):
        """Test contains keyword."""
        schema = array_schema(
            contains=string_schema(pattern=r"^test"), min_contains=1, max_contains=3
        )

        assert schema.contains is not None
        assert schema.min_contains == 1

    def test_dependent_schemas(self):
        """Test dependentSchemas."""
        schema = object_schema(
            properties={"name": string_schema(), "credit_card": string_schema()},
            dependent_schemas={
                "credit_card": object_schema(required=["billing_address"])
            },
        )

        assert "credit_card" in schema.dependent_schemas

    def test_composition_schemas(self):
        """Test allOf, anyOf, oneOf, not."""
        # allOf
        schema = all_of_schema({"type": "string"}, {"minLength": 5})
        assert len(schema.all_of) == 2

        # anyOf
        schema = any_of_schema({"type": "string"}, {"type": "number"})
        assert len(schema.any_of) == 2

        # oneOf
        schema = one_of_schema(string_schema(), number_schema())
        assert len(schema.one_of) == 2

        # not
        schema = not_schema({"type": "null"})
        assert schema.not_ is not None

    def test_conditional(self):
        """Test if/then/else."""
        schema = JSONSchema(
            if_={"type": "string"}, then={"minLength": 5}, else_={"minimum": 0}
        )

        assert schema.if_ is not None
        assert schema.then is not None
        assert schema.else_ is not None


class TestValidationVocabulary:
    """Test validation vocabulary keywords."""

    def test_enum_and_const(self):
        """Test enum and const."""
        enum = enum_schema(["red", "green", "blue"])
        assert len(enum.enum) == 3

        const = const_schema(42)
        assert const.const == 42

    def test_dependent_required(self):
        """Test dependentRequired."""
        schema = object_schema(
            properties={
                "name": string_schema(),
                "credit_card": string_schema(),
                "billing_address": string_schema(),
            },
            dependent_required={"credit_card": ["billing_address"]},
        )

        assert "credit_card" in schema.dependent_required


class TestMetadataVocabulary:
    """Test metadata vocabulary keywords."""

    def test_metadata_annotations(self):
        """Test title, description, default, deprecated, readOnly, writeOnly, examples."""
        schema = string_schema(
            title="Username",
            description="The user's username",
            default="anonymous",
            deprecated=True,
            read_only=False,
            write_only=False,
            examples=["alice", "bob", "charlie"],
        )

        assert schema.title == "Username"
        assert schema.description == "The user's username"
        assert schema.default == "anonymous"
        assert schema.deprecated is True
        assert schema.read_only is False
        assert len(schema.examples) == 3


class TestFormatVocabulary:
    """Test format vocabulary."""

    def test_format_annotation(self):
        """Test format keyword with various standard formats."""
        formats = [
            "date-time",
            "date",
            "time",
            "duration",
            "email",
            "idn-email",
            "hostname",
            "idn-hostname",
            "ipv4",
            "ipv6",
            "uri",
            "uri-reference",
            "iri",
            "iri-reference",
            "uuid",
            "uri-template",
            "json-pointer",
            "relative-json-pointer",
            "regex",
        ]

        for fmt in formats:
            schema = string_schema(format=fmt)
            assert schema.format == fmt


class TestContentVocabulary:
    """Test content vocabulary keywords."""

    def test_content_keywords(self):
        """Test contentEncoding, contentMediaType, contentSchema."""
        schema = string_schema(
            content_encoding="base64",
            content_media_type="application/json",
            content_schema={
                "type": "object",
                "properties": {"message": {"type": "string"}},
            },
        )

        assert schema.content_encoding == "base64"
        assert schema.content_media_type == "application/json"
        assert schema.content_schema is not None


class TestUnevaluatedVocabulary:
    """Test unevaluated vocabulary keywords."""

    def test_unevaluated_properties(self):
        """Test unevaluatedProperties."""
        schema = object_schema(
            properties={"name": string_schema()}, unevaluated_properties=False
        )

        assert schema.unevaluated_properties is False

    def test_unevaluated_items(self):
        """Test unevaluatedItems."""
        schema = array_schema(
            prefix_items=[string_schema(), number_schema()], unevaluated_items=False
        )

        assert schema.unevaluated_items is False


class TestComplexExamples:
    """Test complex real-world schema examples."""

    def test_person_schema(self):
        """Test a complex person schema."""
        schema = JSONSchema(
            schema_="https://json-schema.org/draft/2020-12/schema",
            id="https://example.com/person.schema.json",
            title="Person",
            description="A person object",
            type="object",
            properties={
                "firstName": string_schema(
                    description="The person's first name", min_length=1
                ),
                "lastName": string_schema(
                    description="The person's last name", min_length=1
                ),
                "age": number_schema(
                    description="Age in years", minimum=0, is_integer=True
                ),
                "email": string_schema(format="email", description="Email address"),
                "address": {"$ref": "#/$defs/address"},
            },
            required=["firstName", "lastName"],
            defs={
                "address": object_schema(
                    properties={
                        "street": string_schema(),
                        "city": string_schema(),
                        "state": string_schema(min_length=2, max_length=2),
                        "zipCode": string_schema(pattern=r"^\d{5}(-\d{4})?$"),
                    },
                    required=["street", "city", "state", "zipCode"],
                )
            },
        )

        # Convert to dict and verify structure
        data = schema.model_dump(by_alias=True, exclude_none=True)
        assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert data["title"] == "Person"
        assert "firstName" in data["properties"]
        assert "address" in data["$defs"]

    def test_polymorphic_schema(self):
        """Test a schema with oneOf for polymorphism."""
        schema = JSONSchema(
            one_of=[
                object_schema(
                    properties={
                        "type": const_schema("circle"),
                        "radius": number_schema(minimum=0),
                    },
                    required=["type", "radius"],
                ),
                object_schema(
                    properties={
                        "type": const_schema("rectangle"),
                        "width": number_schema(minimum=0),
                        "height": number_schema(minimum=0),
                    },
                    required=["type", "width", "height"],
                ),
            ]
        )

        assert len(schema.one_of) == 2

    def test_recursive_schema(self):
        """Test a recursive schema (tree structure)."""
        schema = JSONSchema(
            schema_="https://json-schema.org/draft/2020-12/schema",
            id="https://example.com/tree.schema.json",
            type="object",
            properties={
                "value": {},
                "children": {"type": "array", "items": {"$ref": "#"}},
            },
            required=["value"],
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        # Verify the recursive reference
        assert data["properties"]["children"]["items"]["$ref"] == "#"

    def test_conditional_schema(self):
        """Test conditional schema with if/then/else."""
        schema = object_schema(
            properties={"country": string_schema(), "postal_code": string_schema()},
            if_={"properties": {"country": {"const": "US"}}},
            then={"properties": {"postal_code": {"pattern": r"^\d{5}(-\d{4})?$"}}},
            else_={
                "properties": {"postal_code": {"pattern": r"^[A-Z]\d[A-Z] \d[A-Z]\d$"}}
            },
        )

        assert schema.if_ is not None
        assert schema.then is not None
        assert schema.else_ is not None


class TestJSONSerialization:
    """Test JSON serialization and deserialization."""

    def test_serialize_to_json(self):
        """Test serializing schema to JSON."""
        schema = object_schema(
            title="Test Schema",
            properties={
                "name": string_schema(min_length=1),
                "age": number_schema(minimum=0, is_integer=True),
            },
            required=["name"],
        )

        json_str = schema.model_dump_json(by_alias=True, exclude_none=True)
        data = json.loads(json_str)

        assert data["title"] == "Test Schema"
        assert data["type"] == "object"
        assert "name" in data["properties"]

    def test_deserialize_from_json(self):
        """Test deserializing schema from JSON."""
        json_data = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Product",
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "price": {"type": "number", "minimum": 0},
            },
            "required": ["id", "name", "price"],
        }

        schema = JSONSchema(**json_data)

        assert schema.schema_ == "https://json-schema.org/draft/2020-12/schema"
        assert schema.title == "Product"
        assert schema.type == "object"
        assert len(schema.properties) == 3
        assert schema.required == ["id", "name", "price"]

    def test_round_trip(self):
        """Test round-trip serialization."""
        original = object_schema(
            schema_="https://json-schema.org/draft/2020-12/schema",
            id="https://example.com/test.json",
            title="Test",
            properties={"field1": string_schema(), "field2": number_schema(minimum=0)},
            required=["field1"],
        )

        # Serialize
        json_str = original.model_dump_json(by_alias=True, exclude_none=True)

        # Deserialize
        data = json.loads(json_str)
        restored = JSONSchema(**data)

        # Verify
        assert restored.schema_ == original.schema_
        assert restored.id == original.id
        assert restored.title == original.title
        assert len(restored.properties) == len(original.properties)
        assert restored.required == original.required


class TestDeprecatedKeywords:
    """Test deprecated keywords for backward compatibility."""

    def test_definitions(self):
        """Test deprecated 'definitions' keyword."""
        schema = JSONSchema(
            definitions={
                "address": object_schema(properties={"street": string_schema()})
            }
        )

        assert schema.definitions is not None
        assert "address" in schema.definitions

    def test_dependencies(self):
        """Test deprecated 'dependencies' keyword."""
        schema = JSONSchema(
            dependencies={
                "credit_card": ["billing_address"],
                "billing_address": {"type": "object"},
            }
        )

        assert schema.dependencies is not None
        assert "credit_card" in schema.dependencies


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
