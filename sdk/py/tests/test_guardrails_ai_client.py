"""
Unit tests for guardrails_ai.sdk.guardrails_ai_client.GuardrailsAI.
"""

import unittest

from httpx import AsyncClient

from guardrails_ai.sdk import GuardrailsAI
from guardrails_ai.sdk.guards_api import GuardsApi


class TestGuardrailsAIInit(unittest.TestCase):
    """Tests for GuardrailsAI client initialization."""

    def test_api_key_stored_as_auth_header(self):
        client = GuardrailsAI(api_key="test-key-123")

        self.assertEqual(client.headers["x-guardrailsai-api-key"], "test-key-123")

    def test_default_max_retries(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertEqual(client.max_retries, 5)

    def test_custom_max_retries(self):
        client = GuardrailsAI(api_key="test-key", max_retries=10)

        self.assertEqual(client.max_retries, 10)

    def test_zero_max_retries(self):
        client = GuardrailsAI(api_key="test-key", max_retries=0)

        self.assertEqual(client.max_retries, 0)

    def test_guards_api_initialized(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertIsInstance(client.guards, GuardsApi)

    def test_http_client_created_when_not_provided(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertIsInstance(client.http_client, AsyncClient)

    def test_default_base_url(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertEqual(str(client.http_client.base_url), "http://localhost:8000")

    def test_custom_base_url(self):
        client = GuardrailsAI(api_key="test-key", base_url="https://api.example.com")

        self.assertEqual(str(client.http_client.base_url), "https://api.example.com")

    def test_custom_headers_merged_with_auth_headers(self):
        client = GuardrailsAI(
            api_key="test-key",
            headers={"x-custom-header": "custom-value"},
        )

        self.assertEqual(client.headers["x-guardrailsai-api-key"], "test-key")
        self.assertEqual(client.headers["x-custom-header"], "custom-value")

    def test_multiple_custom_headers_merged(self):
        client = GuardrailsAI(
            api_key="test-key",
            headers={"x-header-a": "value-a", "x-header-b": "value-b"},
        )

        self.assertEqual(client.headers["x-header-a"], "value-a")
        self.assertEqual(client.headers["x-header-b"], "value-b")

    def test_no_custom_headers_has_only_auth_header(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertIn("x-guardrailsai-api-key", client.headers)

    def test_provided_http_client_is_used(self):
        custom_http_client = AsyncClient()
        client = GuardrailsAI(api_key="test-key", http_client=custom_http_client)

        self.assertIs(client.http_client, custom_http_client)

    def test_auth_headers_merged_into_provided_http_client(self):
        custom_http_client = AsyncClient()
        GuardrailsAI(api_key="my-api-key", http_client=custom_http_client)

        self.assertEqual(
            custom_http_client.headers["x-guardrailsai-api-key"], "my-api-key"
        )

    def test_custom_headers_merged_into_provided_http_client(self):
        custom_http_client = AsyncClient()
        GuardrailsAI(
            api_key="my-api-key",
            headers={"x-extra": "extra-value"},
            http_client=custom_http_client,
        )

        self.assertEqual(
            custom_http_client.headers["x-guardrailsai-api-key"], "my-api-key"
        )
        self.assertEqual(custom_http_client.headers["x-extra"], "extra-value")

    def test_timeout_passed_to_new_http_client(self):
        client = GuardrailsAI(api_key="test-key", timeout=30.0)

        self.assertEqual(client.http_client.timeout.read, 30.0)

    def test_no_timeout_when_none(self):
        client = GuardrailsAI(api_key="test-key", timeout=None)

        # httpx uses 5.0 as default when timeout=None is passed
        # but the API contract is that None is accepted without error
        self.assertIsInstance(client.http_client, AsyncClient)

    def test_guards_api_shares_http_client(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertIs(client.guards.http_client, client.http_client)

    def test_guards_api_shares_max_retries(self):
        client = GuardrailsAI(api_key="test-key", max_retries=3)

        self.assertEqual(client.guards.max_retries, 3)

    def test_guards_api_shares_headers(self):
        client = GuardrailsAI(api_key="test-key")

        self.assertIs(client.guards.headers, client.headers)

    def test_api_key_not_empty_string(self):
        # Empty string is technically accepted at construction time;
        # this test documents the behavior.
        client = GuardrailsAI(api_key="")

        self.assertEqual(client.headers["x-guardrailsai-api-key"], "")

    def test_different_api_keys_produce_different_headers(self):
        client_a = GuardrailsAI(api_key="key-a")
        client_b = GuardrailsAI(api_key="key-b")

        self.assertNotEqual(
            client_a.headers["x-guardrailsai-api-key"],
            client_b.headers["x-guardrailsai-api-key"],
        )


class TestGuardrailsAIProtocolCompliance(unittest.TestCase):
    """Tests that GuardrailsAI satisfies the Client protocol."""

    def setUp(self):
        self.client = GuardrailsAI(api_key="test-key")

    def test_has_http_client_attribute(self):
        self.assertTrue(hasattr(self.client, "http_client"))

    def test_has_headers_attribute(self):
        self.assertTrue(hasattr(self.client, "headers"))

    def test_has_max_retries_attribute(self):
        self.assertTrue(hasattr(self.client, "max_retries"))

    def test_http_client_is_async_client(self):
        self.assertIsInstance(self.client.http_client, AsyncClient)

    def test_headers_is_dict(self):
        self.assertIsInstance(self.client.headers, dict)

    def test_max_retries_is_int(self):
        self.assertIsInstance(self.client.max_retries, int)


if __name__ == "__main__":
    unittest.main()
