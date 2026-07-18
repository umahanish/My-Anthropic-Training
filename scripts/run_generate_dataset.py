from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

import json
from anthropic import Anthropic

client = Anthropic()
model = "claude-haiku-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if system:
        params["system"] = system
    message = client.messages.create(**params)
    return message.content[0].text


def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a regular expression to complete.

Example output:
```json
[
    {
        "task": "Description of task",
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    print('RAW_RESPONSE:')
    print(text)
    try:
        data = json.loads(text)
        print('\nPARSED JSON:')
        print(json.dumps(data, indent=2))
    except Exception as e:
        print('\nJSON parse failed:', e)


if __name__ == '__main__':
    try:
        generate_dataset()
    except Exception as exc:
        print('Execution error:', type(exc).__name__, exc)
