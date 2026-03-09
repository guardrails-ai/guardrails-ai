from typing import Protocol
from httpx import AsyncClient


class Client(Protocol):
    """Protocol defining the interface shared by all API client classes."""

    http_client: AsyncClient
    headers: dict[str, str]
    max_retries: int
