from typing import Mapping

from httpx import AsyncClient

from guardrails_ai.sdk.abstract_client import Client
from guardrails_ai.sdk.guards_api import GuardsApi


class GuardrailsAI(Client):
    """Main Guardrails AI SDK client with namespaced API access.

    Example::

        client = GuardrailsAI(api_key="your-api-key")
        guard = await client.guards.retrieve(name="my-guard")
        result = await client.guards.validate("my-guard", "some text")
    """

    http_client: AsyncClient
    headers: dict[str, str]
    max_retries: int

    guards: GuardsApi

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "http://localhost:8000",
        timeout: float | None = None,
        max_retries: int = 5,
        headers: Mapping[str, str] | None = None,
        http_client: AsyncClient | None = None,
    ):
        """Initialize the Guardrails AI client.

        Args:
            api_key: Guardrails AI API key for authentication.
            base_url: Base URL for the Guardrails API. Defaults to ``http://localhost:8000``.
            timeout: HTTP request timeout in seconds. Defaults to None (no timeout).
            max_retries: Maximum number of retry attempts for failed requests. Defaults to 5.
            headers: Additional HTTP headers to include with every request.
            http_client: A pre-configured ``httpx.AsyncClient`` to use instead of the
                default. If provided, the required auth headers will be merged into its
                headers.
        """
        # Setup Http Client
        self.max_retries = max_retries
        _headers = {"x-guardrailsai-api-key": api_key}

        ## Merge with any provided headers with required headers
        if headers:
            _headers.update(headers)

        self.headers = _headers

        if not http_client:
            self.http_client = AsyncClient(
                base_url=base_url, headers=self.headers, timeout=timeout
            )
        else:
            http_client.headers.update(self.headers)
            self.http_client = http_client

        # Initialize namespace APIs
        self.guards = GuardsApi(
            http_client=self.http_client,
            headers=self.headers,
            max_retries=self.max_retries,
        )
