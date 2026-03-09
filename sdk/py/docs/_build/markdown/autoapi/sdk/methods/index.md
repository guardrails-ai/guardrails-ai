# sdk.methods

## Functions

| [`get_guard`](#sdk.methods.get_guard)(→ Any)                     | Fetch a Guard by name from the API.       |
|------------------------------------------------------------------|-------------------------------------------|
| [`post_guard_validate`](#sdk.methods.post_guard_validate)(→ Any) | Submit content to a Guard for validation. |

## Module Contents

### *async* sdk.methods.get_guard(, client: httpx.AsyncClient, name: [str](https://docs.python.org/3/library/stdtypes.html#str)) → Any

Fetch a Guard by name from the API.

* **Parameters:**
  * **client** – The async HTTP client to use for the request.
  * **name** – The name of the Guard to retrieve.
* **Returns:**
  The raw JSON response parsed as a Python object.
* **Raises:**
  **httpx.HTTPStatusError** – If the server returns a 4xx or 5xx response.

### *async* sdk.methods.post_guard_validate(, client: httpx.AsyncClient, name: [str](https://docs.python.org/3/library/stdtypes.html#str), body: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]) → Any

Submit content to a Guard for validation.

* **Parameters:**
  * **client** – The async HTTP client to use for the request.
  * **name** – The name of the Guard to validate against.
  * **body** – The request body, including `llmOutput` and any additional fields.
* **Returns:**
  The raw JSON response parsed as a Python object.
* **Raises:**
  **httpx.HTTPStatusError** – If the server returns a 4xx or 5xx response.
