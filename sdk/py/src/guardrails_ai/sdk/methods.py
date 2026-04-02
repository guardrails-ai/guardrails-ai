import httpx
from typing import Any, Optional


async def post_guard(
    *,
    client: httpx.AsyncClient,
    body: dict[str, Any],
) -> Any:
    """Create a Guard via the API.

    Args:
        client: The async HTTP client to use for the request.
        body: The request body to create a Guard.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.post(
        "/guards",
        json=body,
    )
    response.raise_for_status()
    return response.json()


async def get_guard(
    *,
    client: httpx.AsyncClient,
    id: str,
) -> Any:
    """Fetch a Guard by id from the API.

    Args:
        client: The async HTTP client to use for the request.
        id: The id of the Guard to retrieve.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.get(
        f"/guards/{id}",
    )
    response.raise_for_status()
    return response.json()


async def get_guards(
    *,
    client: httpx.AsyncClient,
    name: Optional[str] = None,
) -> Any:
    """Fetch a Guard by id from the API.

    Args:
        client: The async HTTP client to use for the request.
        id: The id of the Guard to retrieve.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    query = f"?name={name}" if name else ""
    response = await client.get(
        f"/guards{query}",
    )
    response.raise_for_status()
    return response.json()


async def put_guard(
    *,
    client: httpx.AsyncClient,
    id: str,
    body: dict[str, Any],
) -> Any:
    """Update a Guard via the API.

    Args:
        client: The async HTTP client to use for the request.
        id: The unique id of the Guard to be updated.
        body: The updated Guard definition.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.put(
        f"/guards/{id}",
        json=body,
    )
    response.raise_for_status()
    return response.json()


async def delete_guard(*, client: httpx.AsyncClient, id: str) -> Any:
    """Delete a Guard via the API.

    Args:
        client: The async HTTP client to use for the request.
        id: The unique id of the Guard to be deleted.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.delete(f"/guards/{id}")
    response.raise_for_status()
    return response.json()


async def post_guard_validate(
    *, client: httpx.AsyncClient, id: str, body: dict[str, Any]
) -> Any:
    """Submit content to a Guard for validation.

    Args:
        client: The async HTTP client to use for the request.
        id: The unique id of the Guard to validate against.
        body: The request body, including ``llm_output`` and any additional fields.

    Returns:
        The raw JSON response parsed as a Python object.

    Raises:
        httpx.HTTPStatusError: If the server returns a 4xx or 5xx response.
    """
    response = await client.post(
        f"/guards/{id}/validate",
        json=body,
    )
    response.raise_for_status()
    return response.json()
