import httpx
from typing import Any


async def get_guard(
    *,
    client: httpx.AsyncClient,
    name: str,
) -> Any:
    """Fetch a Guard by name from the API.

    Args:
        client: The async HTTP client to use for the request.
        name: The name of the Guard to retrieve.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.get(
        f"/guards/{name}",
    )
    response.raise_for_status()
    return response.json()


async def post_guard_validate(
    *, client: httpx.AsyncClient, name: str, body: dict[str, Any]
) -> Any:
    """Submit content to a Guard for validation.

    Args:
        client: The async HTTP client to use for the request.
        name: The name of the Guard to validate against.
        body: The request body, including ``llmOutput`` and any additional fields.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.post(
        f"/guards/{name}/validate",
        json=body,
    )
    response.raise_for_status()
    return response.json()
