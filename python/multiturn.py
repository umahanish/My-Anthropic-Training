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
messages = []

def ask(user_text):
    messages.append({"role": "user", "content": user_text})
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=300,
        temparature=0.7,
        messages=messages,
    )

    text_blocks = [b.text for b in response.content if getattr(b, "type", None) == "text"]

    if not text_blocks:
        block_types = [getattr(b, "type", None) for b in response.content]
        raise ValueError(f"No text blocks returned from Anthropic. Response blocks: {block_types}")

    reply = "".join(text_blocks)
    messages.append({"role": "assistant", "content": reply})
    print(f"Claude: {reply}\n")

ask("My name is Priya and I work on the Nimbus migration project. Remember that.")
ask("What's my name and what project am I working on?")