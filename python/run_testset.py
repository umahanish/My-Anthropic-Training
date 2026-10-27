import os
from pathlib import Path

from dotenv import dotenv_values
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY") or dotenv_values(
    Path(__file__).resolve().parents[1] / ".env"
).get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is missing. Set it in the environment or the repository .env file."
    )

client = Anthropic(api_key=api_key)

contracts = [
    "Nimbus Cloud Services, ends Sept 25 2026, auto-renews unless cancelled 30 days prior.",
    "BrightPath Security Solutions, ends Oct 10 2026, auto-renews unless cancelled 45 days prior.",
    "Vertex Networking Group, ends Nov 5 2026, auto-renews unless cancelled 60 days prior.",
    "Alderwood Office Supplies, ends Dec 15 2026, auto-renews unless cancelled 60 days prior.",
    "Fixed-Term Consulting LLC, ends Sept 20 2026, fixed term, does not auto-renew.",
]

for contract in contracts:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                "Classify this contract's renewal risk as HIGH, MEDIUM, "
                f"or LOW. Assume today is August 1, 2026.\n\n{contract}"
            ),
        }],
    )
    text = next(b.text for b in response.content if b.type == "text")
    print(f"--- {contract[:40]}...\n{text}\n")  