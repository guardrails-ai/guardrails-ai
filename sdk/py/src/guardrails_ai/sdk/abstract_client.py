from typing import Protocol
from httpx import AsyncClient


class Client(Protocol):
    http_client: AsyncClient
    headers: dict[str, str]
    max_retries: int
