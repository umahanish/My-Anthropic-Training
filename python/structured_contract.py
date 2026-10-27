import json
from dataclasses import dataclass


@dataclass
class _MockBlock:
    type: str
    text: str


@dataclass
class _MockResponse:
    content: list


class MockAnthropic:
    """Stands in for anthropic.Anthropic so this script runs with no API key,
    no network call, and no cost. It doesn't call a model -- it just returns a
    canned JSON string shaped like what the real structured-output call above
    would produce for the hardcoded contract prompt. Swap this for a real
    `Anthropic()` client (see git history) once you have an API key set up.
    """

    class _Messages:
        def create(self, **kwargs):
            extracted = {
                "vendor": "Nimbus Cloud Services",
                "end_date": "2026-09-25",
                "auto_renews": True,
                "notice_days": 30,
                "annual_value": 63000,
            }
            return _MockResponse(content=[_MockBlock(type="text", text=json.dumps(extracted))])

    def __init__(self):
        self.messages = self._Messages()


client = MockAnthropic()

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