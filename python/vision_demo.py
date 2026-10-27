import base64
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError(
        f"ANTHROPIC_API_KEY is not set. Add it to {dotenv_path} or the environment."
    )

client = Anthropic(api_key=api_key)

with open("contract_screenshot.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "What vendor and end date does this contract show?"},
        ],
    }],
)
print(next(b.text for b in response.content if b.type == "text"))