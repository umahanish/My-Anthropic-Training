import os
from pathlib import Path
from anthropic import Anthropic
from collections import Counter
from dotenv import dotenv_values

api_key = os.getenv("ANTHROPIC_API_KEY") or dotenv_values(
    Path(__file__).resolve().parents[2] / ".env"
).get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is missing. Set it in the environment or the repository .env file."
    )

client = Anthropic(api_key=api_key)

claim = "Nimbus Cloud Services (ends Sept 25, 2026, 30-day notice) is 🟡 Monitor as of August 1, 2026."

def vote():
    response = client.messages.create(
        model="claude-sonnet-5", max_tokens=100,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": f"Evaluate this claim as of August 1, 2026 (not today's date). The cancellation deadline is 30 calendar days before the contract end date. Is the claim's status correct for that date? Answer only CORRECT or INCORRECT.\n\n{claim}"}],
    )
    text = next(
        (block.text.strip() for block in response.content if block.type == "text"),
        None,
    )
    if not text:
        block_types = [block.type for block in response.content]
        raise RuntimeError(
            "Anthropic returned no text for a vote "
            f"(stop_reason={response.stop_reason!r}, content_types={block_types})."
        )
    return text

votes = [vote() for _ in range(3)]
print("Votes:", votes)
print("Majority:", Counter(votes).most_common(1)[0][0])