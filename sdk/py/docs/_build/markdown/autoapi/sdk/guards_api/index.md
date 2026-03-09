# sdk.guards_api

## Classes

| [`ChatApi`](#sdk.guards_api.ChatApi)               | Namespaced chat API, mirroring the OpenAI `chat` namespace.     |
|----------------------------------------------------|-----------------------------------------------------------------|
| [`CompletionsApi`](#sdk.guards_api.CompletionsApi) | Guarded chat completions, mirroring the OpenAI completions API. |
| [`GuardsApi`](#sdk.guards_api.GuardsApi)           | API for managing Guards and running validations.                |

## Module Contents

### *class* sdk.guards_api.ChatApi(, http_client: httpx.AsyncClient, headers: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)], max_retries: [int](https://docs.python.org/3/library/functions.html#int))

Bases: `guardrails_ai.sdk.abstract_client.Client`

Namespaced chat API, mirroring the OpenAI `chat` namespace.

Accessed via `client.guards.chat`.

#### completions *: [CompletionsApi](#sdk.guards_api.CompletionsApi)*

#### headers *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

#### http_client *: httpx.AsyncClient*

#### max_retries *: [int](https://docs.python.org/3/library/functions.html#int)*

### *class* sdk.guards_api.CompletionsApi(, http_client: httpx.AsyncClient, headers: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)], max_retries: [int](https://docs.python.org/3/library/functions.html#int))

Bases: `guardrails_ai.sdk.abstract_client.Client`

Guarded chat completions, mirroring the OpenAI completions API.

Accessed via `client.guards.chat.completions`.

#### *async* create(guard_name: [str](https://docs.python.org/3/library/stdtypes.html#str), \*\*kwargs: Unpack[openai.types.completion_create_params.CompletionCreateParamsStreaming]) → openai.AsyncStream[openai.types.chat.ChatCompletionChunk]

#### *async* create(guard_name: [str](https://docs.python.org/3/library/stdtypes.html#str), \*\*kwargs: Unpack[openai.types.completion_create_params.CompletionCreateParamsNonStreaming]) → openai.types.chat.ChatCompletion

Create a guarded chat completion.

Proxies the request through the Guardrails API so that the response is
validated by the named Guard before being returned to the caller.

* **Parameters:**
  * **guard_name** – The name of the Guard to apply to the completion.
  * **stream** – If `True`, returns an async stream of `ChatCompletionChunk`
    objects. Defaults to `False`.
  * **\*\*kwargs** – Additional keyword arguments forwarded to the OpenAI
    `chat.completions.create` call (e.g. `model`, `messages`).
* **Returns:**
  A `ChatCompletion` when `stream=False`, or an
  `AsyncStream[ChatCompletionChunk]` when `stream=True`.

Example:

```default
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
```

#### headers *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

#### http_client *: httpx.AsyncClient*

#### max_retries *: [int](https://docs.python.org/3/library/functions.html#int)*

### *class* sdk.guards_api.GuardsApi(, http_client: httpx.AsyncClient, headers: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)], max_retries: [int](https://docs.python.org/3/library/functions.html#int))

Bases: `guardrails_ai.sdk.abstract_client.Client`

API for managing Guards and running validations.

Accessed via `client.guards`.

#### *async* retrieve(name: [str](https://docs.python.org/3/library/stdtypes.html#str)) → guardrails_ai.sdk.types.Guard

Fetch a Guard by name from the Guardrails API.

Retries with exponential back-off up to `max_retries` times on failure.

* **Parameters:**
  **name** – The name of the Guard to retrieve.
* **Returns:**
  A validated `Guard` instance.
* **Raises:**
  **tenacity.RetryError** – If all retry attempts are exhausted.

#### *async* validate(name: [str](https://docs.python.org/3/library/stdtypes.html#str), content: [str](https://docs.python.org/3/library/stdtypes.html#str), \*\*kwargs) → guardrails_ai.sdk.types.ValidationOutcome

Validate content against a Guard.

Retries with exponential back-off up to `max_retries` times on failure.

* **Parameters:**
  * **name** – The name of the Guard to validate against.
  * **content** – The text content (typically LLM output) to validate.
  * **\*\*kwargs** – Additional fields merged into the request body.
* **Returns:**
  A `ValidationOutcome` describing whether validation passed and,
  if so, the validated output.
* **Raises:**
  **tenacity.RetryError** – If all retry attempts are exhausted.

#### chat *: [ChatApi](#sdk.guards_api.ChatApi)*

#### headers *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

#### http_client *: httpx.AsyncClient*

#### max_retries *: [int](https://docs.python.org/3/library/functions.html#int)*
