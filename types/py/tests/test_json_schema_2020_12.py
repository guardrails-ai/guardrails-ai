"""
Test and example usage of JSON Schema Draft 2020-12 Pydantic models.
"""

import json
import unittest

from pydantic import ValidationError

from guardrails_ai.types.json_schema_2020_12 import (
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


class TestBasicSchemas(unittest.TestCase):
    """Test basic schema creation and validation."""

    def test_boolean_schemas(self):
        """Test boolean schemas (true validates all, false validates none)."""
        always_valid = create_boolean_schema(True)
        never_valid = create_boolean_schema(False)

        self.assertIs(always_valid, True)
        self.assertIs(never_valid, False)

    def test_empty_schema(self):
        """Test empty schema (equivalent to true)."""
        schema = JSONSchema()
        self.assertEqual(schema.model_dump(exclude_none=True, by_alias=True), {})

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

        self.assertEqual(schema.type, "string")
        self.assertEqual(schema.min_length, 1)
        self.assertEqual(schema.max_length, 100)
        self.assertEqual(schema.pattern, r"^[a-zA-Z]+$")
        self.assertEqual(schema.format, "email")

    def test_number_schema(self):
        """Test number and integer schemas."""
        int_schema = number_schema(
            minimum=0, maximum=100, multiple_of=5, is_integer=True
        )

        self.assertEqual(int_schema.type, "integer")
        self.assertEqual(int_schema.minimum, 0)
        self.assertEqual(int_schema.maximum, 100)
        self.assertEqual(int_schema.multiple_of, 5)

        float_schema = number_schema(exclusive_minimum=0.0, exclusive_maximum=1.0)

        self.assertEqual(float_schema.type, "number")
        self.assertEqual(float_schema.exclusive_minimum, 0.0)
        self.assertEqual(float_schema.exclusive_maximum, 1.0)

    def test_array_schema(self):
        """Test array schema with item constraints."""
        schema = array_schema(
            items={"type": "string"}, min_items=1, max_items=10, unique_items=True
        )

        self.assertEqual(schema.type, "array")
        self.assertEqual(schema.items.model_dump(exclude_none=True), {"type": "string"})
        self.assertEqual(schema.min_items, 1)
        self.assertEqual(schema.max_items, 10)
        self.assertIs(schema.unique_items, True)

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

        self.assertEqual(schema.type, "object")
        self.assertIn("name", schema.properties)
        self.assertIn("age", schema.properties)
        self.assertIn("email", schema.properties)
        self.assertEqual(schema.required, ["name", "email"])
        self.assertIs(schema.additional_properties, False)


class TestValidation(unittest.TestCase):
    """Test validation of schema constraints."""

    def test_type_validation(self):
        """Test type field validation."""
        # Valid single type
        schema = JSONSchema(type="string")
        self.assertEqual(schema.type, "string")

        # Valid array of types
        schema = JSONSchema(type=["string", "number"])
        self.assertEqual(schema.type, ["string", "number"])

        # Invalid type
        with self.assertRaises(ValidationError):
            JSONSchema(type="invalid")

        # Invalid type in array
        with self.assertRaises(ValidationError):
            JSONSchema(type=["string", "invalid"])

        # Duplicate types
        with self.assertRaises(ValidationError):
            JSONSchema(type=["string", "string"])

    def test_length_constraints(self):
        """Test min/max length validation."""
        # Valid
        schema = JSONSchema(min_length=1, max_length=10)
        self.assertEqual(schema.min_length, 1)

        # Invalid: min > max
        with self.assertRaises(ValidationError):
            JSONSchema(min_length=10, max_length=1)

    def test_items_constraints(self):
        """Test min/max items validation."""
        # Valid
        schema = JSONSchema(min_items=1, max_items=10)
        self.assertEqual(schema.min_items, 1)

        # Invalid: min > max
        with self.assertRaises(ValidationError):
            JSONSchema(min_items=10, max_items=1)

    def test_properties_constraints(self):
        """Test min/max properties validation."""
        # Valid
        schema = JSONSchema(min_properties=1, max_properties=10)
        self.assertEqual(schema.min_properties, 1)

        # Invalid: min > max
        with self.assertRaises(ValidationError):
            JSONSchema(min_properties=10, max_properties=1)

    def test_numeric_constraints(self):
        """Test numeric constraint validation."""
        # Valid
        schema = JSONSchema(minimum=0, maximum=100)
        self.assertEqual(schema.minimum, 0)

        # Invalid: min > max
        with self.assertRaises(ValidationError):
            JSONSchema(minimum=100, maximum=0)

        # Valid exclusive
        schema = JSONSchema(exclusive_minimum=0, exclusive_maximum=100)
        self.assertEqual(schema.exclusive_minimum, 0)

        # Invalid exclusive: min >= max
        with self.assertRaises(ValidationError):
            JSONSchema(exclusive_minimum=100, exclusive_maximum=100)

    def test_contains_constraints(self):
        """Test contains with minContains and maxContains."""
        # Valid
        schema = JSONSchema(contains={"type": "string"}, min_contains=1, max_contains=5)
        self.assertEqual(schema.min_contains, 1)

        # Invalid: minContains without contains
        with self.assertRaises(ValidationError):
            JSONSchema(min_contains=1)

        # Invalid: minContains > maxContains
        with self.assertRaises(ValidationError):
            JSONSchema(contains={"type": "string"}, min_contains=5, max_contains=1)

    def test_conditional_constraints(self):
        """Test if/then/else validation."""
        # Valid
        schema = JSONSchema(
            if_={"type": "string"}, then={"minLength": 5}, else_={"minLength": 10}
        )
        self.assertIsNotNone(schema.if_)

        # Invalid: then without if
        with self.assertRaises(ValidationError):
            JSONSchema(then={"minLength": 5})


class TestCoreVocabulary(unittest.TestCase):
    """Test core vocabulary keywords."""

    def test_schema_and_id(self):
        """Test $schema and $id keywords."""
        schema = JSONSchema(
            schema_="https://json-schema.org/draft/2020-12/schema",
            id="https://example.com/schemas/person.json",
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(
            data["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(data["$id"], "https://example.com/schemas/person.json")

    def test_ref(self):
        """Test $ref keyword."""
        schema = ref_schema("#/$defs/address")

        data = schema.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(data["$ref"], "#/$defs/address")

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
        self.assertIn("$defs", data)
        self.assertIn("address", data["$defs"])

    def test_anchor_and_dynamic_anchor(self):
        """Test $anchor and $dynamicAnchor keywords."""
        schema = JSONSchema(
            anchor="myAnchor", dynamic_anchor="dynamicAnchor", type="string"
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(data["$anchor"], "myAnchor")
        self.assertEqual(data["$dynamicAnchor"], "dynamicAnchor")

    def test_comment(self):
        """Test $comment keyword."""
        schema = JSONSchema(
            comment="This is a comment for schema authors", type="string"
        )

        data = schema.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(data["$comment"], "This is a comment for schema authors")

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
        self.assertIn("$vocabulary", data)
        self.assertEqual(len(data["$vocabulary"]), 4)


class TestApplicatorVocabulary(unittest.TestCase):
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

        self.assertIn("name", schema.properties)
        self.assertEqual(len(schema.pattern_properties), 2)

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

        self.assertEqual(len(schema.prefix_items), 3)
        self.assertIs(schema.items, False)

    def test_contains(self):
        """Test contains keyword."""
        schema = array_schema(
            contains=string_schema(pattern=r"^test"), min_contains=1, max_contains=3
        )

        self.assertIsNotNone(schema.contains)
        self.assertEqual(schema.min_contains, 1)

    def test_dependent_schemas(self):
        """Test dependentSchemas."""
        schema = object_schema(
            properties={"name": string_schema(), "credit_card": string_schema()},
            dependent_schemas={
                "credit_card": object_schema(required=["billing_address"])
            },
        )

        self.assertIn("credit_card", schema.dependent_schemas)

    def test_composition_schemas(self):
        """Test allOf, anyOf, oneOf, not."""
        # allOf
        schema = all_of_schema({"type": "string"}, {"minLength": 5})
        self.assertEqual(len(schema.all_of), 2)

        # anyOf
        schema = any_of_schema({"type": "string"}, {"type": "number"})
        self.assertEqual(len(schema.any_of), 2)

        # oneOf
        schema = one_of_schema(string_schema(), number_schema())
        self.assertEqual(len(schema.one_of), 2)

        # not
        schema = not_schema({"type": "null"})
        self.assertIsNotNone(schema.not_)

    def test_conditional(self):
        """Test if/then/else."""
        schema = JSONSchema(
            if_={"type": "string"}, then={"minLength": 5}, else_={"minimum": 0}
        )

        self.assertIsNotNone(schema.if_)
        self.assertIsNotNone(schema.then)
        self.assertIsNotNone(schema.else_)


class TestValidationVocabulary(unittest.TestCase):
    """Test validation vocabulary keywords."""

    def test_enum_and_const(self):
        """Test enum and const."""
        enum = enum_schema(["red", "green", "blue"])
        self.assertEqual(len(enum.enum), 3)

        const = const_schema(42)
        self.assertEqual(const.const, 42)

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

        self.assertIn("credit_card", schema.dependent_required)


class TestMetadataVocabulary(unittest.TestCase):
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

        self.assertEqual(schema.title, "Username")
        self.assertEqual(schema.description, "The user's username")
        self.assertEqual(schema.default, "anonymous")
        self.assertIs(schema.deprecated, True)
        self.assertIs(schema.read_only, False)
        self.assertEqual(len(schema.examples), 3)


class TestFormatVocabulary(unittest.TestCase):
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
            self.assertEqual(schema.format, fmt)


class TestContentVocabulary(unittest.TestCase):
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

        self.assertEqual(schema.content_encoding, "base64")
        self.assertEqual(schema.content_media_type, "application/json")
        self.assertIsNotNone(schema.content_schema)


class TestUnevaluatedVocabulary(unittest.TestCase):
    """Test unevaluated vocabulary keywords."""

    def test_unevaluated_properties(self):
        """Test unevaluatedProperties."""
        schema = object_schema(
            properties={"name": string_schema()}, unevaluated_properties=False
        )

        self.assertIs(schema.unevaluated_properties, False)

    def test_unevaluated_items(self):
        """Test unevaluatedItems."""
        schema = array_schema(
            prefix_items=[string_schema(), number_schema()], unevaluated_items=False
        )

        self.assertIs(schema.unevaluated_items, False)


class TestComplexExamples(unittest.TestCase):
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
        self.assertEqual(
            data["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(data["title"], "Person")
        self.assertIn("firstName", data["properties"])
        self.assertIn("address", data["$defs"])

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

        self.assertEqual(len(schema.one_of), 2)

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
        self.assertEqual(data["properties"]["children"]["items"]["$ref"], "#")

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

        self.assertIsNotNone(schema.if_)
        self.assertIsNotNone(schema.then)
        self.assertIsNotNone(schema.else_)


class TestJSONSerialization(unittest.TestCase):
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

        self.assertEqual(data["title"], "Test Schema")
        self.assertEqual(data["type"], "object")
        self.assertIn("name", data["properties"])

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

        self.assertEqual(schema.schema_, "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema.title, "Product")
        self.assertEqual(schema.type, "object")
        self.assertEqual(len(schema.properties), 3)
        self.assertEqual(schema.required, ["id", "name", "price"])

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
        self.assertEqual(restored.schema_, original.schema_)
        self.assertEqual(restored.id, original.id)
        self.assertEqual(restored.title, original.title)
        self.assertEqual(len(restored.properties), len(original.properties))
        self.assertEqual(restored.required, original.required)


class TestDeprecatedKeywords(unittest.TestCase):
    """Test deprecated keywords for backward compatibility."""

    def test_definitions(self):
        """Test deprecated 'definitions' keyword."""
        schema = JSONSchema(
            definitions={
                "address": object_schema(properties={"street": string_schema()})
            }
        )

        self.assertIsNotNone(schema.definitions)
        self.assertIn("address", schema.definitions)

    def test_dependencies(self):
        """Test deprecated 'dependencies' keyword."""
        schema = JSONSchema(
            dependencies={
                "credit_card": ["billing_address"],
                "billing_address": {"type": "object"},
            }
        )

        self.assertIsNotNone(schema.dependencies)
        self.assertIn("credit_card", schema.dependencies)


if __name__ == "__main__":
    unittest.main()
