# Guardrails AI SDK

Python SDK for the [Guardrails AI](https://www.guardrailsai.com) API.

## Installation

```bash
pip install guardrails-ai-sdk
```

## Quick Start

```python
import asyncio
from guardrails_ai.sdk import GuardrailsAI

client = GuardrailsAI(api_key="your-api-key")

async def main():
    # Retrieve a guard
    guard = await client.guards.retrieve("my-guard")

    # Validate content
    result = await client.guards.validate("my-guard", "Content to validate")
    print(result.validation_passed)

asyncio.run(main())
```

## Guarded Chat Completions

```python
async def main():
    response = await client.guards.chat.completions.create(
        guard_name="my-guard",
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(chat_completion.guardrails)
    print(chat_completion.choices[0].message.content)
```

## Contents

## Reference

* [API Reference](autoapi/index.md)
  * [sdk](autoapi/sdk/index.md)
