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

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": (
                "Extract this contract: Nimbus Cloud Services, contract "
                "NCS-2025-0142, ends Sept 25 2026, auto-renews unless "
                "cancelled 30 days prior, $63,000/year."
            ),
        }
    ],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "vendor": {"type": "string"},
                    "end_date": {"type": "string"},
                    "auto_renews": {"type": "boolean"},
                    "notice_days": {"type": "integer"},
                    "annual_value": {"type": "number"},
                },
                "required": [
                    "vendor", "end_date", "auto_renews",
                    "notice_days", "annual_value",
                ],
                "additionalProperties": False,
            },
        }
    },
)
print(next(b.text for b in response.content if b.type == "text"))