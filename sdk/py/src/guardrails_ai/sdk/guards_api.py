from typing import Any

from httpx import AsyncClient
from guardrails_ai.sdk.types import Guard, ValidationOutcome
from guardrails_ai.sdk.methods import get_guard, post_guard_validate
from guardrails_ai.sdk.abstract_client import Client
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)


class GuardsApi(Client):
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

    async def retrieve(self, name: str) -> Guard:
        guard_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(get_guard)(client=self.http_client, name=name)

        return Guard.model_validate(guard_any)

    async def validate(self, name: str, content: str, **kwargs) -> None:
        body = {"llmOutput": content, **kwargs}
        validation_outcome_any: Any = await retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=60),
        )(post_guard_validate)(client=self.http_client, name=name, body=body)

        return ValidationOutcome.model_validate(validation_outcome_any)

    # TODO
    async def chat_completion(self, name: str, **kwargs) -> None:
        pass
