"""
Unit tests for guardrails_ai.sdk.methods.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock

import httpx

from guardrails_ai.sdk.methods import get_guard, post_guard_validate


def make_mock_client():
    return AsyncMock(spec=httpx.AsyncClient)


def make_ok_response(data: dict) -> MagicMock:
    response = MagicMock()
    response.json.return_value = data
    response.raise_for_status = MagicMock()
    return response


def make_error_response(status_code: int) -> MagicMock:
    request = httpx.Request("GET", "http://localhost:8000/guards/test")
    raw_response = MagicMock()
    raw_response.status_code = status_code
    error_response = httpx.Response(
        status_code=status_code,
        content=b"error",
        request=request,
    )
    response = MagicMock()
    response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message=f"HTTP {status_code}",
        request=request,
        response=error_response,
    )
    return response


class TestGetGuard(unittest.IsolatedAsyncioTestCase):
    """Tests for the get_guard HTTP helper function."""

    async def test_returns_parsed_json_on_success(self):
        guard_data = {"id": "g1", "name": "my-guard", "validators": []}
        client = make_mock_client()
        client.get.return_value = make_ok_response(guard_data)

        result = await get_guard(client=client, name="my-guard")

        self.assertEqual(result, guard_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.get.return_value = make_ok_response({})

        await get_guard(client=client, name="my-guard")

        client.get.assert_called_once_with("/guards/my-guard")

    async def test_url_uses_provided_guard_name(self):
        client = make_mock_client()
        client.get.return_value = make_ok_response({})

        await get_guard(client=client, name="another-guard")

        client.get.assert_called_once_with("/guards/another-guard")

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.get.return_value = response

        await get_guard(client=client, name="my-guard")

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_404(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(404)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guard(client=client, name="missing-guard")

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guard(client=client, name="my-guard")

    async def test_raises_http_status_error_on_401(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(401)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guard(client=client, name="my-guard")

    async def test_returns_complex_guard_data(self):
        guard_data = {
            "id": "g123",
            "name": "regex-guard",
            "description": "Validates regex patterns",
            "validators": [
                {
                    "id": "guardrails/regex_match",
                    "on": "output",
                    "onFail": "noop",
                    "args": ["\\d+"],
                    "kwargs": {},
                }
            ],
            "output_schema": {"type": "string"},
        }
        client = make_mock_client()
        client.get.return_value = make_ok_response(guard_data)

        result = await get_guard(client=client, name="regex-guard")

        self.assertEqual(result, guard_data)


class TestPostGuardValidate(unittest.IsolatedAsyncioTestCase):
    """Tests for the post_guard_validate HTTP helper function."""

    async def test_returns_parsed_json_on_success(self):
        outcome_data = {
            "callId": "call-1",
            "validatedOutput": "hello",
            "validationPassed": True,
        }
        client = make_mock_client()
        client.post.return_value = make_ok_response(outcome_data)

        result = await post_guard_validate(
            client=client, name="my-guard", body={"llmOutput": "hello"}
        )

        self.assertEqual(result, outcome_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(
            client=client, name="my-guard", body={"llmOutput": "hello"}
        )

        client.post.assert_called_once_with(
            "/guards/my-guard/validate", json={"llmOutput": "hello"}
        )

    async def test_url_uses_provided_guard_name(self):
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(
            client=client, name="another-guard", body={"llmOutput": "world"}
        )

        client.post.assert_called_once_with(
            "/guards/another-guard/validate", json={"llmOutput": "world"}
        )

    async def test_sends_body_as_json(self):
        body = {"llmOutput": "test output", "extra": "param"}
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(client=client, name="my-guard", body=body)

        _, call_kwargs = client.post.call_args
        self.assertEqual(call_kwargs["json"], body)

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.post.return_value = response

        await post_guard_validate(
            client=client, name="my-guard", body={"llmOutput": "hello"}
        )

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_404(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(404)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard_validate(
                client=client, name="missing-guard", body={"llmOutput": "test"}
            )

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard_validate(
                client=client, name="my-guard", body={"llmOutput": "test"}
            )

    async def test_raises_http_status_error_on_422(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(422)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard_validate(
                client=client, name="my-guard", body={"llmOutput": "test"}
            )

    async def test_passes_arbitrary_body_fields(self):
        body = {"llmOutput": "output", "metadata": {"source": "llm"}, "threshold": 0.9}
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(client=client, name="my-guard", body=body)

        _, call_kwargs = client.post.call_args
        self.assertEqual(call_kwargs["json"]["metadata"], {"source": "llm"})
        self.assertEqual(call_kwargs["json"]["threshold"], 0.9)


if __name__ == "__main__":
    unittest.main()
