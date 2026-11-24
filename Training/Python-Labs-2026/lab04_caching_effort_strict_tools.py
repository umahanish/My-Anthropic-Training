"""Lab 4b (Module 4): prompt caching, effort, and strict tools (the replacement for forced tool use).

Part A  Prompt caching: send the same large prefix twice; the second call reads it from cache.
Part B  Effort: the same question at effort low and high; compare output tokens and latency.
Part C  Forced tool use is rejected on the 5.5 models (HTTP 400). Use strict tools with
        tool_choice auto and a clear instruction instead.

Run
    python lab04_caching_effort_strict_tools.py --mock
    python lab04_caching_effort_strict_tools.py            # live
"""
from __future__ import annotations

import json
import time

from common import SONNET, cost_usd, get_client, mock_mode, text_of
from contracts import CONTRACTS, describe

# A large, stable prefix: the policy handbook plus every contract, repeated as a reference appendix.
HANDBOOK = "\n".join(
    [f"Procurement handbook, section {i}: vendor renewals must be reviewed by the owning team "
     f"at least 14 days before the cancellation deadline, and every cancellation is sent in writing."
     for i in range(1, 121)]
    + [describe(c) for c in CONTRACTS]
)

LOOKUP_TOOL = {
    "name": "check_contract_status",
    "description": "Look up a vendor contract. Use it for every question about a specific vendor's dates or terms.",
    "strict": True,  # tool input is guaranteed to match the schema
    "input_schema": {
        "type": "object",
        "properties": {"vendor_name": {"type": "string"}},
        "required": ["vendor_name"],
        "additionalProperties": False,
    },
}


def part_a_caching(client) -> None:
    print("== Part A: prompt caching")
    system = [{"type": "text", "text": HANDBOOK, "cache_control": {"type": "ephemeral"}}]
    for attempt in (1, 2):
        t0 = time.perf_counter()
        resp = client.messages.create(
            model=SONNET,
            max_tokens=200,
            system=system,
            messages=[{"role": "user", "content": "How many days before a deadline must the owning team review a renewal?"}],
        )
        u = resp.usage
        print(f"  call {attempt}: {time.perf_counter() - t0:.2f}s  input={u.input_tokens}  "
              f"cache_write={u.cache_creation_input_tokens}  cache_read={u.cache_read_input_tokens}")
    print("  Expect call 1 to write the cache and call 2 to read it. Cached reads are billed at a fraction of input price.\n")


def part_b_effort(client) -> None:
    print("== Part B: effort")
    question = "Which two contracts need action first, and why? Answer in three sentences.\n" + "\n".join(describe(c) for c in CONTRACTS)
    for effort in ("low", "high"):
        t0 = time.perf_counter()
        resp = client.messages.create(
            model=SONNET,
            max_tokens=2000,
            output_config={"effort": effort},
            messages=[{"role": "user", "content": question}],
        )
        u = resp.usage
        print(f"  effort={effort:5} {time.perf_counter() - t0:5.2f}s  output_tokens={u.output_tokens:5}  "
              f"cost=${cost_usd(SONNET, u.input_tokens, u.output_tokens):.5f}")
    print("  Higher effort spends more tokens on reasoning. Pick the lowest effort that passes your evals.\n")


def part_c_strict_tools(client) -> None:
    print("== Part C: forced tool use vs strict tools")
    if not mock_mode():
        from anthropic import BadRequestError

        try:
            client.messages.create(
                model=SONNET, max_tokens=200, tools=[LOOKUP_TOOL],
                tool_choice={"type": "tool", "name": "check_contract_status"},
                messages=[{"role": "user", "content": "Nimbus status?"}],
            )
            print("  forced tool_choice was accepted (unexpected for 5.5 models)")
        except BadRequestError as err:
            print(f"  forced tool_choice -> 400 as documented: {str(err)[:110]}...")
    else:
        print("  forced tool_choice -> 400 invalid_request_error (shown live only)")

    resp = client.messages.create(
        model=SONNET,
        max_tokens=300,
        system="Always call check_contract_status before answering a question about a vendor.",
        tools=[LOOKUP_TOOL],
        tool_choice={"type": "auto"},
        messages=[{"role": "user", "content": "When does the Nimbus Cloud Services contract end?"}],
    )
    calls = [b for b in resp.content if b.type == "tool_use"]
    if calls:
        print(f"  strict tool call: {calls[0].name}({json.dumps(calls[0].input)})  stop_reason={resp.stop_reason}")
    else:
        print(f"  no tool call; model answered directly: {text_of(resp)[:80]}")


def mock_responder(kw: dict):
    if kw.get("tools"):
        return [{"type": "tool_use", "id": "toolu_mock", "name": "check_contract_status",
                 "input": {"vendor_name": "Nimbus Cloud Services"}}]
    return "Review at least 14 days before the cancellation deadline."


if __name__ == "__main__":
    client = get_client(mock_responder)
    part_a_caching(client)
    part_b_effort(client)
    part_c_strict_tools(client)
