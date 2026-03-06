import httpx
from typing import Any


async def get_guard(
    *,
    client: httpx.AsyncClient,
    name: str,
) -> Any:
    response = await client.get(
        f"/guards/{name}",
    )
    response.raise_for_status()
    return response.json()


async def post_guard_validate(
    *,
    client: httpx.AsyncClient,
    name: str,
) -> Any:
    response = await client.post(
        f"/guards/{name}/validate",
    )
    response.raise_for_status()
    return response.json()
