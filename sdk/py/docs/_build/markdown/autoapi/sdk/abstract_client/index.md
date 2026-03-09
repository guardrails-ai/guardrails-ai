# sdk.abstract_client

## Classes

| [`Client`](#sdk.abstract_client.Client)   | Protocol defining the interface shared by all API client classes.   |
|-------------------------------------------|---------------------------------------------------------------------|

## Module Contents

### *class* sdk.abstract_client.Client

Bases: `Protocol`

Protocol defining the interface shared by all API client classes.

#### headers *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

#### http_client *: httpx.AsyncClient*

#### max_retries *: [int](https://docs.python.org/3/library/functions.html#int)*
