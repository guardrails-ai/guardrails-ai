# sdk.guardrails_ai_client

## Classes

| [`GuardrailsAI`](#sdk.guardrails_ai_client.GuardrailsAI)   | Main Guardrails AI SDK client with namespaced API access.   |
|------------------------------------------------------------|-------------------------------------------------------------|

## Module Contents

### *class* sdk.guardrails_ai_client.GuardrailsAI(, api_key: [str](https://docs.python.org/3/library/stdtypes.html#str), base_url: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'http://localhost:8000', timeout: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None) = None, max_retries: [int](https://docs.python.org/3/library/functions.html#int) = 5, headers: Mapping[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)] | [None](https://docs.python.org/3/library/constants.html#None) = None, http_client: httpx.AsyncClient | [None](https://docs.python.org/3/library/constants.html#None) = None)

Bases: `guardrails_ai.sdk.abstract_client.Client`

Main Guardrails AI SDK client with namespaced API access.

Example:

```default
client = GuardrailsAI(api_key="your-api-key")
guard = await client.guards.retrieve(name="my-guard")
result = await client.guards.validate("my-guard", "some text")
```

Initialize the Guardrails AI client.

* **Parameters:**
  * **api_key** – Guardrails AI API key for authentication.
  * **base_url** – Base URL for the Guardrails API. Defaults to `http://localhost:8000`.
  * **timeout** – HTTP request timeout in seconds. Defaults to None (no timeout).
  * **max_retries** – Maximum number of retry attempts for failed requests. Defaults to 5.
  * **headers** – Additional HTTP headers to include with every request.
  * **http_client** – A pre-configured `httpx.AsyncClient` to use instead of the
    default. If provided, the required auth headers will be merged into its
    headers.

#### guards *: guardrails_ai.sdk.guards_api.GuardsApi*

#### headers *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

#### http_client *: httpx.AsyncClient*

#### max_retries *: [int](https://docs.python.org/3/library/functions.html#int)*
