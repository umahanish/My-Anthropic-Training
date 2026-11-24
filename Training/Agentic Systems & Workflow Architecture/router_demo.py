import os
from pathlib import Path

from dotenv import dotenv_values
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY") or dotenv_values(
    Path(__file__).resolve().parents[2] / ".env"
).get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is missing. Set it in the environment or the repository .env file."
    )

client = Anthropic(api_key=api_key)

def response_text(response) -> str:
    text = next(
        (block.text.strip() for block in response.content if block.type == "text"),
        None,
    )
    if not text:
        block_types = [block.type for block in response.content]
        raise RuntimeError(
            "Anthropic returned no text "
            f"(stop_reason={response.stop_reason!r}, content_types={block_types})."
        )
    return text

def classify(question: str) -> str:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001", max_tokens=20,
        messages=[{"role": "user", "content": (
            "Classify this question as SIMPLE (a direct lookup) or COMPLEX "
            f"(needs multi-step reasoning). Answer with one word.\n\n{question}"
        )}],
    )
    return response_text(response)

def route(question: str) -> str:
    category = classify(question)
    is_simple = "SIMPLE" in category.upper()  # robust to punctuation like "SIMPLE."
    model = "claude-haiku-4-5-20251001" if is_simple else "claude-sonnet-5"
    print(f"[{category} -> routed to {model}]")
    response = client.messages.create(model=model, max_tokens=300, messages=[{"role": "user", "content": question}])
    return response_text(response)

print(route("What's the annual value of the Nimbus Cloud Services contract?"))
print(route("Given all 5 course contracts, which combination of cancellations would save the most money this year while keeping at least one security-related vendor active?"))