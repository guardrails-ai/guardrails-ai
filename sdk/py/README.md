# guardrails-client
A thin REST client for the guardrails-api.

## Quickstart

```sh
pip install guardrails-ai-sdk
```

```py
from guardrails_ai.sdk import GuardrailsAI, Guard, ValidationOutcome

# Init the GuardrailsAI client
client = GuardrailsAI(api_key="xxx")

# Fetch a Guard from the server
guard: Guard = await client.guards.retrieve(name="my-guard")

print(guard)

# Run a Guard to validate content
validation_outcome: ValidationOutcome = await client.guards.validate(name="my-guard", llm_output="Hello, world.")

if not validation_outcome.validation_passed:
    print(validation_outcome.validation_summaries)

# Create Guarded Chat Completions
chat_completion = await client.guards.chat.completions.create(guard_name="my-guard", model="gpt-5-nano", messages=[{ "role": "user", "content": "Hello, world." }])

print(chat_completion.choices[0].message.content)
print(chat_completion.guardrails)

# Stream Guarded Chat Completions
completion_stream = await client.guards.chat.completions.create(
    guard_name="my-first-guard",
    model="gpt-5-nano",
    messages=[
        {"role": "user", "content": "Give yourself a realistic name and introduce yourself."}
    ],
    stream=True
)

full_text = ""
validation_summaries = []
async for chunk in completion_stream:
    full_text += chunk.choices[0].delta.content
    validation_summaries.extend(chunk.guardrails.get("validation_summaries", []))


print("\n ==> Validation Summaries: ", validation_summaries)
print("\n ==> Final Content: ", full_text)
```