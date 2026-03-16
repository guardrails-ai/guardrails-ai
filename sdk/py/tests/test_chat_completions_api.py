"""
Unit tests for guardrails_ai.sdk.chat_completions_api (ChatApi, CompletionsApi).
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient

from guardrails_ai.sdk.chat_completions_api import CompletionsApi, ChatApi


def make_http_client() -> AsyncClient:
    return AsyncClient(base_url="http://localhost:8000")


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
            "guardrails_ai.sdk.chat_completions_api.AsyncOpenAIClient",
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
            "guardrails_ai.sdk.chat_completions_api.AsyncOpenAIClient",
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
            "guardrails_ai.sdk.chat_completions_api.AsyncOpenAIClient",
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


if __name__ == "__main__":
    unittest.main()
