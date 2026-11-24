"""Shared setup for the Python labs.

Models and API rules for the 5.5 family:
- Do not pass temperature, top_p or top_k (non-default values return HTTP 400).
- Do not send thinking={"type": "disabled"} (Sonnet 5.5 rejects it).
- Use the claude-*-5-5 IDs below.
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

HAIKU = "claude-haiku-5-5"
SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"

load_dotenv(Path(__file__).resolve().parent / ".env")


def get_client():
    """Return an Anthropic client, or exit with a clear message if no key is set."""
    from anthropic import Anthropic

    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Put it in labs/.env or export it in your shell.")
    return Anthropic()


def text_of(response) -> str:
    """Join the text blocks of a Messages response, or fail with the block types seen."""
    parts = [b.text for b in response.content if b.type == "text"]
    if not parts:
        types = [b.type for b in response.content]
        raise RuntimeError(f"No text returned (stop_reason={response.stop_reason!r}, blocks={types})")
    return "".join(parts).strip()
