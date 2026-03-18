"""
Unit tests for guardrails_ai.sdk.guards_api
"""

import unittest
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient

from guardrails_ai.sdk.guards_api import GuardsApi
from guardrails_ai.sdk.chat_completions_api import ChatApi, CompletionsApi
from guardrails_ai.types import Guard, ValidationOutcome, CreateGuardRequest


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
            result = await api.retrieve("g1")

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
            await api.retrieve("g1")

        call_kwargs = mock_get.call_args.kwargs
        self.assertEqual(call_kwargs["id"], "g1")

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
            await api.retrieve("g1")

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
            result = await api.retrieve("g2")

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
                result = await api.retrieve("g1")

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
                    await api.retrieve("g1")

        self.assertEqual(mock_get.call_count, 2)

    async def test_guard_description_is_none_when_not_provided(self):
        api = make_guards_api()
        guard_data_no_desc = {"id": "g3", "name": "no-desc-guard", "validators": []}

        with patch(
            "guardrails_ai.sdk.guards_api.get_guard",
            new_callable=AsyncMock,
            return_value=guard_data_no_desc,
        ):
            result = await api.retrieve("g3")

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
        self.assertEqual(call_kwargs["id"], "specific-guard")

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
# GuardsApi — create
# ---------------------------------------------------------------------------


class TestGuardsApiCreate(unittest.IsolatedAsyncioTestCase):
    async def test_returns_guard_on_success(self):
        api = make_guards_api()
        request = CreateGuardRequest(name="new-guard")

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ):
            result = await api.create(request)

        self.assertIsInstance(result, Guard)
        self.assertEqual(result.id, "g1")
        self.assertEqual(result.name, "test-guard")

    async def test_passes_serialized_body_to_post_guard(self):
        api = make_guards_api()
        request = CreateGuardRequest(name="my-guard", description="desc")

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_post:
            await api.create(request)

        call_kwargs = mock_post.call_args.kwargs
        self.assertEqual(call_kwargs["body"]["name"], "my-guard")
        self.assertEqual(call_kwargs["body"]["description"], "desc")

    async def test_passes_http_client_to_post_guard(self):
        http_client = make_http_client()
        api = GuardsApi(http_client=http_client, headers={}, max_retries=1)
        request = CreateGuardRequest(name="my-guard")

        with patch(
            "guardrails_ai.sdk.guards_api.post_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_post:
            await api.create(request)

        self.assertIs(mock_post.call_args.kwargs["client"], http_client)

    async def test_retries_and_succeeds_on_transient_failure(self):
        api = GuardsApi(http_client=make_http_client(), headers={}, max_retries=3)
        request = CreateGuardRequest(name="my-guard")

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.post_guard",
                new_callable=AsyncMock,
                side_effect=[Exception("transient"), GUARD_DATA],
            ) as mock_post:
                result = await api.create(request)

        self.assertEqual(mock_post.call_count, 2)
        self.assertIsInstance(result, Guard)

    async def test_raises_after_max_retries_exhausted(self):
        api = GuardsApi(http_client=make_http_client(), headers={}, max_retries=2)
        request = CreateGuardRequest(name="my-guard")

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.post_guard",
                new_callable=AsyncMock,
                side_effect=Exception("always fails"),
            ) as mock_post:
                with self.assertRaises(Exception):
                    await api.create(request)

        self.assertEqual(mock_post.call_count, 2)


# ---------------------------------------------------------------------------
# GuardsApi — list
# ---------------------------------------------------------------------------


class TestGuardsApiList(unittest.IsolatedAsyncioTestCase):
    async def test_returns_list_of_guards_on_success(self):
        api = make_guards_api()
        guards_data = [GUARD_DATA, {**GUARD_DATA, "id": "g2", "name": "other-guard"}]

        with patch(
            "guardrails_ai.sdk.guards_api.get_guards",
            new_callable=AsyncMock,
            return_value=guards_data,
        ):
            result = await api.list()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Guard)
        self.assertEqual(result[0].id, "g1")

    async def test_returns_empty_list_when_no_guards(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.get_guards",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await api.list()

        self.assertEqual(result, [])

    async def test_passes_none_name_by_default(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.get_guards",
            new_callable=AsyncMock,
            return_value=[],
        ) as mock_get:
            await api.list()

        self.assertIsNone(mock_get.call_args.kwargs["name"])

    async def test_passes_name_filter_when_provided(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.get_guards",
            new_callable=AsyncMock,
            return_value=[GUARD_DATA],
        ) as mock_get:
            await api.list(name="test-guard")

        self.assertEqual(mock_get.call_args.kwargs["name"], "test-guard")

    async def test_passes_http_client_to_get_guards(self):
        http_client = make_http_client()
        api = GuardsApi(http_client=http_client, headers={}, max_retries=1)

        with patch(
            "guardrails_ai.sdk.guards_api.get_guards",
            new_callable=AsyncMock,
            return_value=[],
        ) as mock_get:
            await api.list()

        self.assertIs(mock_get.call_args.kwargs["client"], http_client)

    async def test_retries_and_succeeds_on_transient_failure(self):
        api = GuardsApi(http_client=make_http_client(), headers={}, max_retries=3)

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.get_guards",
                new_callable=AsyncMock,
                side_effect=[Exception("transient"), [GUARD_DATA]],
            ) as mock_get:
                result = await api.list()

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(len(result), 1)


# ---------------------------------------------------------------------------
# GuardsApi — update
# ---------------------------------------------------------------------------


class TestGuardsApiUpdate(unittest.IsolatedAsyncioTestCase):
    async def test_returns_guard_on_success(self):
        api = make_guards_api()
        guard = Guard(**GUARD_DATA)

        with patch(
            "guardrails_ai.sdk.guards_api.put_guard",
            new_callable=AsyncMock,
            return_value={**GUARD_DATA, "name": "updated-guard"},
        ):
            result = await api.update(guard)

        self.assertIsInstance(result, Guard)
        self.assertEqual(result.name, "updated-guard")

    async def test_passes_guard_id_to_put_guard(self):
        api = make_guards_api()
        guard = Guard(**GUARD_DATA)

        with patch(
            "guardrails_ai.sdk.guards_api.put_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_put:
            await api.update(guard)

        self.assertEqual(mock_put.call_args.kwargs["id"], "g1")

    async def test_passes_serialized_guard_as_body(self):
        api = make_guards_api()
        guard = Guard(**GUARD_DATA)

        with patch(
            "guardrails_ai.sdk.guards_api.put_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_put:
            await api.update(guard)

        body = mock_put.call_args.kwargs["body"]
        self.assertEqual(body["name"], "test-guard")

    async def test_passes_http_client_to_put_guard(self):
        http_client = make_http_client()
        api = GuardsApi(http_client=http_client, headers={}, max_retries=1)
        guard = Guard(**GUARD_DATA)

        with patch(
            "guardrails_ai.sdk.guards_api.put_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_put:
            await api.update(guard)

        self.assertIs(mock_put.call_args.kwargs["client"], http_client)

    async def test_retries_and_succeeds_on_transient_failure(self):
        api = GuardsApi(http_client=make_http_client(), headers={}, max_retries=3)
        guard = Guard(**GUARD_DATA)

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.put_guard",
                new_callable=AsyncMock,
                side_effect=[Exception("transient"), GUARD_DATA],
            ) as mock_put:
                result = await api.update(guard)

        self.assertEqual(mock_put.call_count, 2)
        self.assertIsInstance(result, Guard)


# ---------------------------------------------------------------------------
# GuardsApi — delete
# ---------------------------------------------------------------------------


class TestGuardsApiDelete(unittest.IsolatedAsyncioTestCase):
    async def test_returns_guard_on_success(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.delete_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ):
            result = await api.delete("g1")

        self.assertIsInstance(result, Guard)
        self.assertEqual(result.id, "g1")

    async def test_passes_id_to_delete_guard(self):
        api = make_guards_api()

        with patch(
            "guardrails_ai.sdk.guards_api.delete_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_del:
            await api.delete("g1")

        self.assertEqual(mock_del.call_args.kwargs["id"], "g1")

    async def test_passes_http_client_to_delete_guard(self):
        http_client = make_http_client()
        api = GuardsApi(http_client=http_client, headers={}, max_retries=1)

        with patch(
            "guardrails_ai.sdk.guards_api.delete_guard",
            new_callable=AsyncMock,
            return_value=GUARD_DATA,
        ) as mock_del:
            await api.delete("g1")

        self.assertIs(mock_del.call_args.kwargs["client"], http_client)

    async def test_retries_and_succeeds_on_transient_failure(self):
        api = GuardsApi(http_client=make_http_client(), headers={}, max_retries=3)

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.delete_guard",
                new_callable=AsyncMock,
                side_effect=[Exception("transient"), GUARD_DATA],
            ) as mock_del:
                result = await api.delete("g1")

        self.assertEqual(mock_del.call_count, 2)
        self.assertIsInstance(result, Guard)

    async def test_raises_after_max_retries_exhausted(self):
        api = GuardsApi(http_client=make_http_client(), headers={}, max_retries=2)

        with patch(
            "guardrails_ai.sdk.guards_api.wait_exponential",
            return_value=__import__("tenacity").wait_none(),
        ):
            with patch(
                "guardrails_ai.sdk.guards_api.delete_guard",
                new_callable=AsyncMock,
                side_effect=Exception("always fails"),
            ) as mock_del:
                with self.assertRaises(Exception):
                    await api.delete("g1")

        self.assertEqual(mock_del.call_count, 2)


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
