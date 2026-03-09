from typing import Any, Unpack, overload
from httpx import AsyncClient
from guardrails_ai.sdk.types import Guard, ValidationOutcome
from guardrails_ai.sdk.methods import get_guard, post_guard_validate
from guardrails_ai.sdk.abstract_client import Client
from openai import AsyncClient as AsyncOpenAIClient, AsyncStream
from openai.types.completion_create_params import (
    CompletionCreateParamsStreaming,
    CompletionCreateParamsNonStreaming,
)
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)


class CompletionsApi(Client):
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
        self, guard_name: str, **kwargs: Unpack[CompletionCreateParamsStreaming]
    ) -> AsyncStream[ChatCompletionChunk]: ...
    @overload
    async def create(
        self, guard_name: str, **kwargs: Unpack[CompletionCreateParamsNonStreaming]
    ) -> ChatCompletion: ...
    async def create(
        self, guard_name: str, **kwargs: Unpack[CompletionCreateParamsNonStreaming]
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        openai_client = AsyncOpenAIClient(
            base_url=f"{self.http_client.base_url}/guards/{guard_name}/openai/v1",
            http_client=self.http_client,
            max_retries=self.max_retries,
        )
        return await openai_client.chat.completions.create(**kwargs)


class ChatApi(Client):
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


class GuardsApi(Client):
    http_client: AsyncClient
    headers: dict[str, str]
    max_retries: int
    chat: ChatApi

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
        self.chat = ChatApi(
            http_client=http_client, headers=headers, max_retries=max_retries
        )

    async def retrieve(self, name: str) -> Guard:
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(get_guard)(client=self.http_client, name=name)

        return Guard.model_validate(guard_any)

    async def validate(self, name: str, content: str, **kwargs) -> ValidationOutcome:
        body = {"llmOutput": content, **kwargs}
        validation_outcome_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(post_guard_validate)(client=self.http_client, name=name, body=body)

        return ValidationOutcome.model_validate(validation_outcome_any)
