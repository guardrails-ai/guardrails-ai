from typing import Any, Optional
from guardrails_ai.sdk.chat_completions_api import ChatApi
from httpx import AsyncClient
from guardrails_ai.types import Guard, ValidationOutcome, CreateGuardRequest
from guardrails_ai.sdk.methods import (
    delete_guard,
    get_guard,
    get_guards,
    post_guard,
    post_guard_validate,
    put_guard,
)
from guardrails_ai.sdk.abstract_client import Client
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
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

    async def create(self, guard: CreateGuardRequest) -> Guard:
        """Creates a Guard on the Guardrails API.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            guard: The request body of the Guard to create.

        Returns:
            A validated ``Guard`` instance.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(post_guard)(client=self.http_client, body=guard.model_dump())

        return Guard.model_validate(guard_any)

    async def retrieve(self, id: str) -> Guard:
        """Fetch a Guard by id from the Guardrails API.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            id: The id of the Guard to retrieve.

        Returns:
            A validated ``Guard`` instance.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(get_guard)(client=self.http_client, id=id)

        return Guard.model_validate(guard_any)

    async def list(self, *, name: Optional[str] = None) -> list[Guard]:
        """List Guards from the Guardrails API.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            name: If provided, will fetch guards only with the designated name.  Defaults to None.

        Returns:
            A validated list of ``Guard`` instances.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        guards_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(get_guards)(client=self.http_client, name=name)

        return [Guard.model_validate(g) for g in guards_any]

    async def update(self, guard: Guard) -> Guard:
        """Updates a Guard on the Guardrails API.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            guard: The updated Guard to persist.

        Returns:
            A validated ``Guard`` instance.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(put_guard)(client=self.http_client, id=guard.id, body=guard.model_dump())

        return Guard.model_validate(guard_any)

    async def delete(self, id: str) -> Guard:
        """Deletes a Guard on the Guardrails API.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            id: The unique id of the Guard to delete.

        Returns:
            A validated ``Guard`` instance.

        Raises:
            tenacity.RetryError: If all retry attempts are exhausted.
        """
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(delete_guard)(client=self.http_client, id=id)

        return Guard.model_validate(guard_any)

    async def validate(self, id: str, content: str, **kwargs) -> ValidationOutcome:
        """Validate content against a Guard.

        Retries with exponential back-off up to ``max_retries`` times on failure.

        Args:
            id: The unique id of the Guard to validate against.
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
        )(post_guard_validate)(client=self.http_client, id=id, body=body)

        return ValidationOutcome.model_validate(validation_outcome_any)
