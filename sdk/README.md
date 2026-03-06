# guardrails-client
A thin REST client for the guardrails-api.

## Quickstart

```sh
pip install guardrails-ai-sdk
```

```py
from guardrails_ai.sdk import GuardrailsAI, Guard, ValidationOutcome

client = GuardrailsAI(api_key="xxx")

# Fetch a Guard from the server
guard: Guard = client.guards.retrieve(name="my-guard")

print(guard)

# Run a Guard to validate content
validation_outcome: ValidationOutcome = client.guards.validate(name="my-guard", llm_output="Hello, world.")

if not validation_outcome.validation_passed:
    print(validation_outcome.validation_summaries)

# Make Guarded ChatCompletions calls
chat_completion = client.guards.chat_completion(name="my-guard", model="gpt-5-nano", messages=[{ "role": "user", "content": "Hello, world." }])

print(chat_completion.choices[0].message.content)
print(chat_completion.guardrails)
```

