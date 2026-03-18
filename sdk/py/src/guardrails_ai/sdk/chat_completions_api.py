from typing import Optional, Unpack, overload
from guardrails_ai.types import ValidationOutcome
from httpx import AsyncClient
from guardrails_ai.sdk.abstract_client import Client
from openai import AsyncClient as AsyncOpenAIClient, AsyncStream
from openai.types.completion_create_params import (
    CompletionCreateParamsStreaming,
    CompletionCreateParamsNonStreaming,
    CompletionCreateParamsBase,
)
from openai.types.chat import ChatCompletion, ChatCompletionChunk


class GuardedChatCompletion(ChatCompletion):
    guardrails: Optional[ValidationOutcome]


class GuardedChatCompletionChunk(ChatCompletionChunk):
    guardrails: Optional[ValidationOutcome]


class CompletionsApi(Client):
    """Guarded chat completions, mirroring the OpenAI completions API.

    Accessed via ``client.guards.chat.completions``.
    """

    http_client: AsyncClient
    headers: dict[str, str]
    max_retries: int

    def __init__(
        self,
        *,
        http_client: AsyncClient,
        headers: dict[str, str],
        max_retries: int,
    ):
        self.http_client = http_client
        self.headers = headers
        self.max_retries = max_retries

    @overload
    async def create(
        self, guard_id: str, **kwargs: Unpack[CompletionCreateParamsStreaming]
    ) -> AsyncStream[GuardedChatCompletionChunk]: ...
    @overload
    async def create(
        self, guard_id: str, **kwargs: Unpack[CompletionCreateParamsNonStreaming]
    ) -> GuardedChatCompletion: ...
    async def create(
        self,
        guard_id: str,
        *,
        stream: Optional[bool] = False,
        **kwargs: Unpack[CompletionCreateParamsBase],
    ) -> GuardedChatCompletion | AsyncStream[GuardedChatCompletionChunk]:
        """Create a guarded chat completion.

        Proxies the request through the Guardrails API so that the response is
        validated by the named Guard before being returned to the caller.

        Args:
            guard_id: The unique id of the Guard to apply to the completion.
            stream: If ``True``, returns an async stream of ``GuardedChatCompletionChunk``
                objects. Defaults to ``False``.
            **kwargs: Additional keyword arguments forwarded to the OpenAI
                ``chat.completions.create`` call (e.g. ``model``, ``messages``).

        Returns:
            A ``GuardedChatCompletion`` when ``stream=False``, or an
            ``AsyncStream[GuardedChatCompletionChunk]`` when ``stream=True``.

        Example::

            # Non-streaming
            response = await client.guards.chat.completions.create(
                guard_id="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello!"}],
            )

            # Streaming
            async for chunk in await client.guards.chat.completions.create(
                guard_id="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello!"}],
                stream=True,
            ):
                print(chunk)
        """
        openai_client = AsyncOpenAIClient(
            base_url=f"{self.http_client.base_url}/guards/{guard_id}/openai/v1",
            http_client=self.http_client,
            max_retries=self.max_retries,
        )
        return await openai_client.chat.completions.create(stream=stream, **kwargs)  # type: ignore


class ChatApi(Client):
    """Namespaced chat API, mirroring the OpenAI ``chat`` namespace.

    Accessed via ``client.guards.chat``.
    """

    http_client: AsyncClient
    headers: dict[str, str]
    max_retries: int
    completions: CompletionsApi

    def __init__(
        self,
        *,
        http_client: AsyncClient,
        headers: dict[str, str],
        max_retries: int,
    ):
        self.http_client = http_client
        self.headers = headers
        self.max_retries = max_retries
        self.completions = CompletionsApi(
            http_client=http_client, headers=headers, max_retries=max_retries
        )
