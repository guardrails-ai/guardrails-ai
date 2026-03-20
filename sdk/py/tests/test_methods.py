"""
Unit tests for guardrails_ai.sdk.methods.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock

import httpx

from guardrails_ai.sdk.methods import (
    delete_guard,
    get_guard,
    get_guards,
    post_guard,
    post_guard_validate,
    put_guard,
)


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

        result = await get_guard(client=client, id="g1")

        self.assertEqual(result, guard_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.get.return_value = make_ok_response({})

        await get_guard(client=client, id="g1")

        client.get.assert_called_once_with("/guards/g1")

    async def test_url_uses_provided_guard_name(self):
        client = make_mock_client()
        client.get.return_value = make_ok_response({})

        await get_guard(client=client, id="another-guard")

        client.get.assert_called_once_with("/guards/another-guard")

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.get.return_value = response

        await get_guard(client=client, id="g1")

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_404(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(404)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guard(client=client, id="missing-guard")

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guard(client=client, id="g1")

    async def test_raises_http_status_error_on_401(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(401)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guard(client=client, id="g1")

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

        result = await get_guard(client=client, id="g123")

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
            client=client, id="g1", body={"llm_output": "hello"}
        )

        self.assertEqual(result, outcome_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(client=client, id="g1", body={"llm_output": "hello"})

        client.post.assert_called_once_with(
            "/guards/g1/validate", json={"llm_output": "hello"}
        )

    async def test_url_uses_provided_guard_name(self):
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(
            client=client, id="another-guard", body={"llm_output": "world"}
        )

        client.post.assert_called_once_with(
            "/guards/another-guard/validate", json={"llm_output": "world"}
        )

    async def test_sends_body_as_json(self):
        body = {"llm_output": "test output", "extra": "param"}
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(client=client, id="g1", body=body)

        _, call_kwargs = client.post.call_args
        self.assertEqual(call_kwargs["json"], body)

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.post.return_value = response

        await post_guard_validate(client=client, id="g1", body={"llm_output": "hello"})

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_404(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(404)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard_validate(
                client=client, id="missing-guard", body={"llm_output": "test"}
            )

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard_validate(
                client=client, id="g1", body={"llm_output": "test"}
            )

    async def test_raises_http_status_error_on_422(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(422)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard_validate(
                client=client, id="g1", body={"llm_output": "test"}
            )

    async def test_passes_arbitrary_body_fields(self):
        body = {"llm_output": "output", "metadata": {"source": "llm"}, "threshold": 0.9}
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard_validate(client=client, id="g1", body=body)

        _, call_kwargs = client.post.call_args
        self.assertEqual(call_kwargs["json"]["metadata"], {"source": "llm"})
        self.assertEqual(call_kwargs["json"]["threshold"], 0.9)


class TestPostGuard(unittest.IsolatedAsyncioTestCase):
    """Tests for the post_guard HTTP helper function."""

    async def test_returns_parsed_json_on_success(self):
        guard_data = {"id": "g1", "name": "my-guard", "validators": []}
        client = make_mock_client()
        client.post.return_value = make_ok_response(guard_data)

        result = await post_guard(client=client, body={"name": "my-guard"})

        self.assertEqual(result, guard_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard(client=client, body={"name": "my-guard"})

        client.post.assert_called_once_with("/guards", json={"name": "my-guard"})

    async def test_sends_body_as_json(self):
        body = {"name": "my-guard", "description": "A guard"}
        client = make_mock_client()
        client.post.return_value = make_ok_response({})

        await post_guard(client=client, body=body)

        _, call_kwargs = client.post.call_args
        self.assertEqual(call_kwargs["json"], body)

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.post.return_value = response

        await post_guard(client=client, body={"name": "my-guard"})

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_422(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(422)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard(client=client, body={"name": "bad"})

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.post.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await post_guard(client=client, body={"name": "my-guard"})


class TestGetGuards(unittest.IsolatedAsyncioTestCase):
    """Tests for the get_guards HTTP helper function."""

    async def test_returns_parsed_json_on_success(self):
        guards_data = [
            {"id": "g1", "name": "guard-one"},
            {"id": "g2", "name": "guard-two"},
        ]
        client = make_mock_client()
        client.get.return_value = make_ok_response(guards_data)

        result = await get_guards(client=client, name=None)

        self.assertEqual(result, guards_data)

    async def test_calls_guards_endpoint_without_query_when_name_is_none(self):
        client = make_mock_client()
        client.get.return_value = make_ok_response([])

        await get_guards(client=client, name=None)

        client.get.assert_called_once_with("/guards")

    async def test_appends_name_query_param_when_provided(self):
        client = make_mock_client()
        client.get.return_value = make_ok_response([])

        await get_guards(client=client, name="my-guard")

        client.get.assert_called_once_with("/guards?name=my-guard")

    async def test_calls_raise_for_status(self):
        response = make_ok_response([])
        client = make_mock_client()
        client.get.return_value = response

        await get_guards(client=client, name=None)

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.get.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await get_guards(client=client, name=None)


class TestPutGuard(unittest.IsolatedAsyncioTestCase):
    """Tests for the put_guard HTTP helper function."""

    async def test_returns_parsed_json_on_success(self):
        guard_data = {"id": "g1", "name": "updated-guard", "validators": []}
        client = make_mock_client()
        client.put.return_value = make_ok_response(guard_data)

        result = await put_guard(client=client, id="g1", body={"name": "updated-guard"})

        self.assertEqual(result, guard_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.put.return_value = make_ok_response({})

        await put_guard(client=client, id="g1", body={"name": "updated-guard"})

        client.put.assert_called_once_with("/guards/g1", json={"name": "updated-guard"})

    async def test_url_uses_provided_id(self):
        client = make_mock_client()
        client.put.return_value = make_ok_response({})

        await put_guard(client=client, id="another-id", body={})

        client.put.assert_called_once_with("/guards/another-id", json={})

    async def test_sends_body_as_json(self):
        body = {"name": "new-name", "description": "updated"}
        client = make_mock_client()
        client.put.return_value = make_ok_response({})

        await put_guard(client=client, id="g1", body=body)

        _, call_kwargs = client.put.call_args
        self.assertEqual(call_kwargs["json"], body)

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.put.return_value = response

        await put_guard(client=client, id="g1", body={})

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_404(self):
        client = make_mock_client()
        client.put.return_value = make_error_response(404)

        with self.assertRaises(httpx.HTTPStatusError):
            await put_guard(client=client, id="missing", body={})

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.put.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await put_guard(client=client, id="g1", body={})


class TestDeleteGuard(unittest.IsolatedAsyncioTestCase):
    """Tests for the delete_guard HTTP helper function."""

    async def test_returns_parsed_json_on_success(self):
        guard_data = {"id": "g1", "name": "deleted-guard", "validators": []}
        client = make_mock_client()
        client.delete.return_value = make_ok_response(guard_data)

        result = await delete_guard(client=client, id="g1")

        self.assertEqual(result, guard_data)

    async def test_calls_correct_url(self):
        client = make_mock_client()
        client.delete.return_value = make_ok_response({})

        await delete_guard(client=client, id="g1")

        client.delete.assert_called_once_with("/guards/g1")

    async def test_url_uses_provided_id(self):
        client = make_mock_client()
        client.delete.return_value = make_ok_response({})

        await delete_guard(client=client, id="some-other-id")

        client.delete.assert_called_once_with("/guards/some-other-id")

    async def test_calls_raise_for_status(self):
        response = make_ok_response({})
        client = make_mock_client()
        client.delete.return_value = response

        await delete_guard(client=client, id="g1")

        response.raise_for_status.assert_called_once()

    async def test_raises_http_status_error_on_404(self):
        client = make_mock_client()
        client.delete.return_value = make_error_response(404)

        with self.assertRaises(httpx.HTTPStatusError):
            await delete_guard(client=client, id="missing")

    async def test_raises_http_status_error_on_500(self):
        client = make_mock_client()
        client.delete.return_value = make_error_response(500)

        with self.assertRaises(httpx.HTTPStatusError):
            await delete_guard(client=client, id="g1")


if __name__ == "__main__":
    unittest.main()
