"""Shared setup for the Python labs (Claude 5.5 family).

API rules for claude-*-5-5 models (each returns HTTP 400 if broken):
- No temperature, top_p or top_k.
- No thinking={"type": "disabled"} and no thinking budgets. Use output_config={"effort": ...}.
- No forced tool use: tool_choice must be {"type": "auto"} or {"type": "none"}.
- No assistant prefill (last message must not be a partial assistant turn).

Every lab accepts --mock (or LAB_MOCK=1) to run offline with canned responses,
so the code path can be studied before API keys are provisioned.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Callable

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:  # python-dotenv is optional
    pass

HAIKU = "claude-haiku-5-5"
SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"

# USD per million tokens (input, output). Verify against the current pricing page before quoting.
PRICES = {
    HAIKU: (1.00, 5.00),
    SONNET: (2.00, 10.00),
    OPUS: (4.00, 20.00),
}

TODAY = "2026-08-01"  # fixed reference date for the course scenario


def mock_mode() -> bool:
    return "--mock" in sys.argv or os.getenv("LAB_MOCK") == "1"


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000


def text_of(response) -> str:
    """Join the text blocks of a Messages response, or fail with the block types seen."""
    parts = [b.text for b in response.content if b.type == "text"]
    if not parts:
        types = [b.type for b in response.content]
        raise RuntimeError(f"No text returned (stop_reason={response.stop_reason!r}, blocks={types})")
    return "".join(parts).strip()


def json_of(response) -> dict:
    """Parse the text of a structured-output response as JSON."""
    return json.loads(text_of(response))


# ---------------------------------------------------------------- mock client
Responder = Callable[[dict], "str | list"]


def _usage(kw: dict, out_text: str):
    prompt = json.dumps(kw.get("messages", ""), default=str) + str(kw.get("system", ""))
    return SimpleNamespace(
        input_tokens=max(1, len(prompt) // 4),
        output_tokens=max(1, len(out_text) // 4),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
    )


def _response(kw: dict, result) -> SimpleNamespace:
    """A responder returns a string (one text block) or a list of block dicts."""
    if isinstance(result, str):
        blocks = [SimpleNamespace(type="text", text=result)]
    else:
        blocks = [SimpleNamespace(**b) for b in result]
    stop = "tool_use" if any(b.type == "tool_use" for b in blocks) else "end_turn"
    out = "".join(getattr(b, "text", "") or json.dumps(getattr(b, "input", {})) for b in blocks)
    return SimpleNamespace(content=blocks, stop_reason=stop, model=kw.get("model"), usage=_usage(kw, out))


class _MockMessages:
    def __init__(self, responder: Responder, latency: float):
        self._responder, self._latency = responder, latency

    def create(self, **kw):
        time.sleep(self._latency)
        return _response(kw, self._responder(kw))


class _AsyncMockMessages(_MockMessages):
    async def create(self, **kw):  # type: ignore[override]
        await asyncio.sleep(self._latency)
        return _response(kw, self._responder(kw))


def get_client(responder: Responder | None = None, latency: float = 0.2):
    """Real Anthropic client, or a mock when --mock / LAB_MOCK=1 is set."""
    if mock_mode():
        print("[mock mode: no API calls are made]\n")
        return SimpleNamespace(messages=_MockMessages(responder or (lambda kw: "mock reply"), latency))
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Put it in .env, export it, or run with --mock.")
    from anthropic import Anthropic

    return Anthropic()


def get_async_client(responder: Responder | None = None, latency: float = 0.5):
    if mock_mode():
        print("[mock mode: no API calls are made]\n")
        return SimpleNamespace(messages=_AsyncMockMessages(responder or (lambda kw: "mock reply"), latency))
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Put it in .env, export it, or run with --mock.")
    from anthropic import AsyncAnthropic

    return AsyncAnthropic()


def last_user_text(kw: dict) -> str:
    """Helper for mock responders: the text of the latest user message."""
    content = kw["messages"][-1]["content"]
    if isinstance(content, str):
        return content
    return " ".join(str(c.get("text", c.get("content", ""))) for c in content if isinstance(c, dict))
