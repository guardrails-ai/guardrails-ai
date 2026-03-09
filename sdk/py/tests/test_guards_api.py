"""
Unit tests for guardrails_ai.sdk.guards_api (GuardsApi, ChatApi, CompletionsApi).
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient

from guardrails_ai.sdk.guards_api import CompletionsApi, ChatApi, GuardsApi
from guardrails_ai.sdk.types import Guard, ValidationOutcome


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

GUARD_DATA = {
    "id": "g1",
    "name": "test-guard",
    "description": "A test guard",
    "validators": [],
}

VALIDATION_OUTCOME_DATA = {
    "callId": "call-1",
    "rawLlmOutput": "raw output",
    "validatedOutput": "validated output",
    "validationPassed": True,
    "validationSummaries": [],
    "reask": None,
    "error": None,
}


def make_http_client() -> AsyncClient:
    return AsyncClient(base_url="http://localhost:8000")


def make_guards_api(max_retries: int = 1) -> GuardsApi:
    return GuardsApi(
        http_client=make_http_client(),
        headers={"x-guardrailsai-api-key": "test-key"},
        max_retries=max_retries,
    )


# ---------------------------------------------------------------------------
# CompletionsApi
# ---------------------------------------------------------------------------


class TestCompletionsApiInit(unittest.TestCase):
    def test_stores_http_client(self):
        http_client = make_http_client()
        api = CompletionsApi(
            http_client=http_client,
            headers={"x-guardrailsai-api-key": "key"},
            max_retries=3,
        )
        self.assertIs(api.http_client, http_client)

    def test_stores_headers(self):
        headers = {"x-guardrailsai-api-key": "key", "x-custom": "value"}
        api = CompletionsApi(
            http_client=make_http_client(),
            headers=headers,
            max_retries=3,
        )
        self.assertEqual(api.headers, headers)

    def test_stores_max_retries(self):
        api = CompletionsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=7,
        )
        self.assertEqual(api.max_retries, 7)


class TestCompletionsApiCreate(unittest.IsolatedAsyncioTestCase):
    async def test_create_instantiates_openai_client_with_guard_base_url(self):
        http_client = make_http_client()
        api = CompletionsApi(
            http_client=http_client,
            headers={"x-guardrailsai-api-key": "key"},
            max_retries=2,
        )

        mock_chat_completion = MagicMock()
        mock_openai_instance = MagicMock()
        mock_openai_instance.chat.completions.create = AsyncMock(
            return_value=mock_chat_completion
        )

        with patch(
            "guardrails_ai.sdk.guards_api.AsyncOpenAIClient",
            return_value=mock_openai_instance,
        ) as MockOpenAIClient:
            result = await api.create(
                "my-guard",
                model="gpt-4",
                messages=[{"role": "user", "content": "hello"}],
            )

        MockOpenAIClient.assert_called_once_with(
            base_url=f"{http_client.base_url}/guards/my-guard/openai/v1",
            http_client=http_client,
            max_retries=2,
        )
        self.assertIs(result, mock_chat_completion)

    async def test_create_passes_kwargs_to_openai_create(self):
        http_client = make_http_client()
        api = CompletionsApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )

        mock_openai_instance = MagicMock()
        mock_openai_instance.chat.completions.create = AsyncMock(return_value=None)

        with patch(
            "guardrails_ai.sdk.guards_api.AsyncOpenAIClient",
            return_value=mock_openai_instance,
        ):
            await api.create(
                "my-guard",
                model="gpt-4",
                messages=[{"role": "user", "content": "hello"}],
                temperature=0.5,
            )

        mock_openai_instance.chat.completions.create.assert_called_once_with(
            stream=False,
            model="gpt-4",
            messages=[{"role": "user", "content": "hello"}],
            temperature=0.5,
        )

    async def test_create_uses_correct_guard_name_in_url(self):
        http_client = make_http_client()
        api = CompletionsApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )

        mock_openai_instance = MagicMock()
        mock_openai_instance.chat.completions.create = AsyncMock(return_value=None)

        with patch(
            "guardrails_ai.sdk.guards_api.AsyncOpenAIClient",
            return_value=mock_openai_instance,
        ) as MockOpenAIClient:
            await api.create("special-guard", model="gpt-4", messages=[])

        call_kwargs = MockOpenAIClient.call_args.kwargs
        self.assertIn("special-guard", call_kwargs["base_url"])


# ---------------------------------------------------------------------------
# ChatApi
# ---------------------------------------------------------------------------


class TestChatApiInit(unittest.TestCase):
    def test_stores_http_client(self):
        http_client = make_http_client()
        api = ChatApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )
        self.assertIs(api.http_client, http_client)

    def test_stores_headers(self):
        headers = {"x-key": "val"}
        api = ChatApi(
            http_client=make_http_client(),
            headers=headers,
            max_retries=1,
        )
        self.assertEqual(api.headers, headers)

    def test_stores_max_retries(self):
        api = ChatApi(
            http_client=make_http_client(),
            headers={},
            max_retries=4,
        )
        self.assertEqual(api.max_retries, 4)

    def test_completions_api_initialized(self):
        api = ChatApi(
            http_client=make_http_client(),
            headers={},
            max_retries=1,
        )
        self.assertIsInstance(api.completions, CompletionsApi)

    def test_completions_api_shares_http_client(self):
        http_client = make_http_client()
        api = ChatApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )
        self.assertIs(api.completions.http_client, http_client)

    def test_completions_api_shares_headers(self):
        headers = {"x-key": "val"}
        api = ChatApi(
            http_client=make_http_client(),
            headers=headers,
            max_retries=1,
        )
        self.assertEqual(api.completions.headers, headers)

    def test_completions_api_shares_max_retries(self):
        api = ChatApi(
            http_client=make_http_client(),
            headers={},
            max_retries=9,
        )
        self.assertEqual(api.completions.max_retries, 9)


# ---------------------------------------------------------------------------
# GuardsApi — init
# ---------------------------------------------------------------------------


class TestGuardsApiInit(unittest.TestCase):
    def test_stores_http_client(self):
        http_client = make_http_client()
        api = GuardsApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )
        self.assertIs(api.http_client, http_client)

    def test_stores_headers(self):
        headers = {"x-guardrailsai-api-key": "k"}
        api = GuardsApi(
            http_client=make_http_client(),
            headers=headers,
            max_retries=1,
        )
        self.assertEqual(api.headers, headers)

    def test_stores_max_retries(self):
        api = GuardsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=6,
        )
        self.assertEqual(api.max_retries, 6)

    def test_chat_api_initialized(self):
        api = make_guards_api()
        self.assertIsInstance(api.chat, ChatApi)

    def test_chat_api_shares_http_client(self):
        http_client = make_http_client()
        api = GuardsApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )
        self.assertIs(api.chat.http_client, http_client)

    def test_chat_api_shares_headers(self):
        headers = {"x-key": "val"}
        api = GuardsApi(
            http_client=make_http_client(),
            headers=headers,
            max_retries=1,
        )
        self.assertEqual(api.chat.headers, headers)

    def test_chat_api_shares_max_retries(self):
        api = GuardsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=8,
        )
        self.assertEqual(api.chat.max_retries, 8)

    def test_chat_completions_api_initialized(self):
        api = make_guards_api()
        self.assertIsInstance(api.chat.completions, CompletionsApi)


# ---------------------------------------------------------------------------
# GuardsApi — retrieve
# ---------------------------------------------------------------------------


class TestGuardsApiRetrieve(unittest.IsolatedAsyncioTestCase):
    async def test_returns_guard_on_success(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.get_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ):
            result = await api.retrieve("test-guard")

        self.assertIsInstance(result, Guard)
        self.assertEqual(result.id, "g1")
        self.assertEqual(result.name, "test-guard")

    async def test_passes_correct_name_to_get_guard(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.get_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_get:
            await api.retrieve("my-guard")

        call_kwargs = mock_get.call_args.kwargs
        self.assertEqual(call_kwargs["name"], "my-guard")

    async def test_passes_http_client_to_get_guard(self):
        http_client = make_http_client()
        api = GuardsApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )

        with patch(
            "guardrails_ai.sdk.guards_api.get_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_get:
            await api.retrieve("test-guard")

        call_kwargs = mock_get.call_args.kwargs
        self.assertIs(call_kwargs["client"], http_client)

    async def test_validates_response_as_guard_model(self):
        api = make_guards_api()
        guard_data = {
            "id": "g2",
            "name": "another-guard",
            "description": "desc",
            "validators": [
                {
                    "id": "guardrails/regex_match",
                    "on": "output",
                    "onFail": "noop",
                    "kwargs": {},
                }
            ],
        }

        with patch(
            "guardrails_ai.sdk.guards_api.get_guard",
            new_callable=AsyncMock,
            return_value=guard_data,
        ):
            result = await api.retrieve("another-guard")

        self.assertIsInstance(result, Guard)
        self.assertEqual(len(result.validators), 1)
        self.assertEqual(result.validators[0].id, "guardrails/regex_match")

    async def test_retries_and_succeeds_on_transient_failure(self):
        api = GuardsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=3,
        )

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.get_guard",
                new_callable=AsyncMock,
                side_effect=[Exception("transient error"), GUARD_DATA],
            ) as mock_get:
                result = await api.retrieve("test-guard")

        self.assertEqual(mock_get.call_count, 2)
        self.assertIsInstance(result, Guard)

    async def test_raises_after_max_retries_exhausted(self):
        api = GuardsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=2,
        )

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.get_guard",
                new_callable=AsyncMock,
                side_effect=Exception("always fails"),
            ) as mock_get:
                with self.assertRaises(Exception):
                    await api.retrieve("test-guard")

        self.assertEqual(mock_get.call_count, 2)

    async def test_guard_description_is_none_when_not_provided(self):
        api = make_guards_api()
        guard_data_no_desc = {"id": "g3", "name": "no-desc-guard", "validators": []}

        with patch(
            "guardrails_ai.sdk.guards_api.get_guard",
            new_callable=AsyncMock,
            return_value=guard_data_no_desc,
        ):
            result = await api.retrieve("no-desc-guard")

        self.assertIsNone(result.description)


# ---------------------------------------------------------------------------
# GuardsApi — validate
# ---------------------------------------------------------------------------


class TestGuardsApiValidate(unittest.IsolatedAsyncioTestCase):
    async def test_returns_validation_outcome_on_success(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ):
            result = await api.validate("test-guard", "hello world")

        self.assertIsInstance(result, ValidationOutcome)
        self.assertEqual(result.call_id, "call-1")

    async def test_builds_body_with_llm_output(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ) as mock_post:
            await api.validate("test-guard", "my content")

        call_kwargs = mock_post.call_args.kwargs
        self.assertEqual(call_kwargs["body"]["llmOutput"], "my content")

    async def test_passes_guard_name_to_post(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ) as mock_post:
            await api.validate("specific-guard", "content")

        call_kwargs = mock_post.call_args.kwargs
        self.assertEqual(call_kwargs["name"], "specific-guard")

    async def test_passes_http_client_to_post(self):
        http_client = make_http_client()
        api = GuardsApi(
            http_client=http_client,
            headers={},
            max_retries=1,
        )

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ) as mock_post:
            await api.validate("test-guard", "content")

        call_kwargs = mock_post.call_args.kwargs
        self.assertIs(call_kwargs["client"], http_client)

    async def test_extra_kwargs_merged_into_body(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ) as mock_post:
            await api.validate("test-guard", "content", threshold=0.9, source="test")

        call_kwargs = mock_post.call_args.kwargs
        body = call_kwargs["body"]
        self.assertEqual(body["threshold"], 0.9)
        self.assertEqual(body["source"], "test")

    async def test_validates_response_as_validation_outcome_model(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ):
            result = await api.validate("test-guard", "hello")

        self.assertTrue(result.validation_passed)
        self.assertEqual(result.validated_output, "validated output")
        self.assertEqual(result.raw_llm_output, "raw output")

    async def test_validation_outcome_with_failed_validation(self):
        api = make_guards_api()
        failed_outcome = {
            "callId": "call-2",
            "rawLlmOutput": "bad output",
            "validatedOutput": None,
            "validationPassed": False,
            "validationSummaries": [
                {
                    "validatorName": "guardrails/regex_match",
                    "validatorStatus": "fail",
                    "propertyPath": "output",
                    "failureReason": "Pattern not matched",
                    "errorSpans": [],
                }
            ],
            "reask": None,
            "error": None,
        }

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=failed_outcome,
        ):
            result = await api.validate("test-guard", "bad output")

        self.assertFalse(result.validation_passed)
        self.assertIsNone(result.validated_output)
        self.assertIsNotNone(result.validation_summaries)
        self.assertEqual(len(result.validation_summaries), 1)

    async def test_retries_and_succeeds_on_transient_failure(self):
        api = GuardsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=3,
        )

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.post_guard_validate",
                new_callable=AsyncMock,
                side_effect=[Exception("transient"), VALIDATION_OUTCOME_DATA],
            ) as mock_post:
                result = await api.validate("test-guard", "content")

        self.assertEqual(mock_post.call_count, 2)
        self.assertIsInstance(result, ValidationOutcome)

    async def test_raises_after_max_retries_exhausted(self):
        api = GuardsApi(
            http_client=make_http_client(),
            headers={},
            max_retries=2,
        )

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.post_guard_validate",
                new_callable=AsyncMock,
                side_effect=Exception("always fails"),
            ) as mock_post:
                with self.assertRaises(Exception):
                    await api.validate("test-guard", "content")

        self.assertEqual(mock_post.call_count, 2)

    async def test_body_only_contains_llm_output_when_no_kwargs(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=VALIDATION_OUTCOME_DATA,
        ) as mock_post:
            await api.validate("test-guard", "just content")

        call_kwargs = mock_post.call_args.kwargs
        self.assertEqual(call_kwargs["body"], {"llmOutput": "just content"})

    async def test_validation_outcome_with_error_field(self):
        api = make_guards_api()
        error_outcome = {
            "callId": "call-err",
            "rawLlmOutput": None,
            "validatedOutput": None,
            "validationPassed": False,
            "validationSummaries": None,
            "reask": None,
            "error": "Unexpected error during validation",
        }

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard_validate",
            new_callable=AsyncMock,
            return_value=error_outcome,
        ):
            result = await api.validate("test-guard", "content")

        self.assertEqual(result.error, "Unexpected error during validation")
        self.assertFalse(result.validation_passed)


# ---------------------------------------------------------------------------
# GuardsApi — protocol compliance
# ---------------------------------------------------------------------------


class TestGuardsApiProtocolCompliance(unittest.TestCase):
    def setUp(self):
        self.api = make_guards_api()

    def test_has_http_client_attribute(self):
        self.assertTrue(hasattr(self.api, "http_client"))

    def test_has_headers_attribute(self):
        self.assertTrue(hasattr(self.api, "headers"))

    def test_has_max_retries_attribute(self):
        self.assertTrue(hasattr(self.api, "max_retries"))

    def test_http_client_is_async_client(self):
        self.assertIsInstance(self.api.http_client, AsyncClient)

    def test_headers_is_dict(self):
        self.assertIsInstance(self.api.headers, dict)

    def test_max_retries_is_int(self):
        self.assertIsInstance(self.api.max_retries, int)


if __name__ == "__main__":
    unittest.main()
