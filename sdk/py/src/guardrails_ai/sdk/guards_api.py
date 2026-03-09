from typing import Any, Optional, Unpack, overload
from httpx import AsyncClient
from guardrails_ai.sdk.types import Guard, ValidationOutcome
from guardrails_ai.sdk.methods import get_guard, post_guard_validate
from guardrails_ai.sdk.abstract_client import Client
from openai import AsyncClient as AsyncOpenAIClient, AsyncStream
from openai.types.completion_create_params import (
    CompletionCreateParamsStreaming,
    CompletionCreateParamsNonStreaming,
    CompletionCreateParamsBase,
)
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)


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
        self, guard_name: str, **kwargs: Unpack[CompletionCreateParamsStreaming]
    ) -> AsyncStream[ChatCompletionChunk]: ...
    @overload
    async def create(
        self, guard_name: str, **kwargs: Unpack[CompletionCreateParamsNonStreaming]
    ) -> ChatCompletion: ...
    async def create(
        self,
        guard_name: str,
        *,
        stream: Optional[bool] = False,
        **kwargs: Unpack[CompletionCreateParamsBase],
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        """Create a guarded chat completion.

        Proxies the request through the Guardrails API so that the response is
        validated by the named Guard before being returned to the caller.

        Args:
            guard_name: The name of the Guard to apply to the completion.
            stream: If ``True``, returns an async stream of ``ChatCompletionChunk``
                objects. Defaults to ``False``.
            **kwargs: Additional keyword arguments forwarded to the OpenAI
                ``chat.completions.create`` call (e.g. ``model``, ``messages``).

        Returns:
            A ``ChatCompletion`` when ``stream=False``, or an
            ``AsyncStream[ChatCompletionChunk]`` when ``stream=True``.

        Example::

            # Non-streaming
            response = await client.guards.chat.completions.create(
                guard_name="my-guard",
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello!"}],
            )

            # Streaming
            async for chunk in await client.guards.chat.completions.create(
                guard_name="my-guard",
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello!"}],
                stream=True,
            ):
                print(chunk)
        """
        openai_client = AsyncOpenAIClient(
            base_url=f"{self.http_client.base_url}/guards/{guard_name}/openai/v1",
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


class GuardsApi(Client):
    """API for managing Guards and running validations.

    Accessed via ``client.guards``.
    """

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
        """Fetch a Guard by name from the Guardrails API.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            name: The name of the Guard to retrieve.

        Returns:
            A validated ``Guard`` instance.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(get_guard)(client=self.http_client, name=name)

        return Guard.model_validate(guard_any)

    async def validate(self, name: str, content: str, **kwargs) -> ValidationOutcome:
        """Validate content against a Guard.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            name: The name of the Guard to validate against.
            content: The text content (typically LLM output) to validate.
            **kwargs: Additional fields merged into the request body.

        Returns:
            A ``ValidationOutcome`` describing whether validation passed and,
            if so, the validated output.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        body = {"llmOutput": content, **kwargs}
        validation_outcome_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(post_guard_validate)(client=self.http_client, name=name, body=body)

        return ValidationOutcome.model_validate(validation_outcome_any)
