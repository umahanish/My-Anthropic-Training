"""Lab 10a (Module 10): trace your own agent.

Claude Code has built-in OpenTelemetry (see the Session 10 guide). Agents you build on the API
need their own tracing. This lab adds spans to a tool loop and writes them as JSON lines, in the
same shape an OpenTelemetry backend would show: one interaction span, with llm and tool spans inside.

Each span records: trace_id, span_id, parent_id, name, duration, model, tokens, cost, status.
Prompt text is redacted unless LOG_PROMPTS=1, the same default Claude Code uses.

Run
    python lab10_tracing.py --mock        # writes traces.jsonl and prints a summary
    python lab10_tracing.py               # live

Exercise: make the lookup tool fail for one vendor (raise an exception) and find the failed span
in traces.jsonl. Which field would you alert on?
"""
from __future__ import annotations

import json
import os
import time
import uuid
from contextlib import contextmanager

from common import SONNET, cost_usd, get_client, text_of
from contracts import CONTRACTS

TRACE_FILE = "traces.jsonl"
LOG_PROMPTS = os.getenv("LOG_PROMPTS") == "1"


class Tracer:
    def __init__(self, path: str):
        self.path, self.stack = path, []
        open(path, "w").close()

    @contextmanager
    def span(self, name: str, **attrs):
        parent = self.stack[-1] if self.stack else None
        record = {
            "trace_id": parent["trace_id"] if parent else uuid.uuid4().hex[:16],
            "span_id": uuid.uuid4().hex[:8],
            "parent_id": parent["span_id"] if parent else None,
            "name": name, "status": "ok", **attrs,
        }
        self.stack.append(record)
        t0 = time.perf_counter()
        try:
            yield record
        except Exception as err:
            record["status"], record["error"] = "error", str(err)[:200]
            raise
        finally:
            record["duration_ms"] = round((time.perf_counter() - t0) * 1000, 1)
            self.stack.pop()
            with open(self.path, "a") as f:
                f.write(json.dumps(record) + "\n")


TOOLS = [{
    "name": "check_contract_status",
    "description": "Look up a vendor contract by vendor name.",
    "input_schema": {"type": "object", "properties": {"vendor_name": {"type": "string"}}, "required": ["vendor_name"]},
}]


def lookup(vendor_name: str) -> str:
    for c in CONTRACTS:
        if c["vendor"].lower() == vendor_name.lower():
            return json.dumps(c)
    return "Not found."


def traced_agent(client, tracer: Tracer, question: str, max_steps: int = 5) -> str:
    with tracer.span("interaction", prompt=question if LOG_PROMPTS else "<REDACTED>") as root:
        messages = [{"role": "user", "content": question}]
        for step in range(max_steps):
            with tracer.span("llm", model=SONNET, step=step) as s:
                resp = client.messages.create(model=SONNET, max_tokens=600, tools=TOOLS, messages=messages)
                s.update(input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens,
                         cost_usd=round(cost_usd(SONNET, resp.usage.input_tokens, resp.usage.output_tokens), 6),
                         stop_reason=resp.stop_reason)
            messages.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason != "tool_use":
                root["steps"] = step + 1
                return text_of(resp)
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    with tracer.span("tool", tool=block.name, args=block.input if LOG_PROMPTS else "<REDACTED>"):
                        out = lookup(**block.input)
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
            messages.append({"role": "user", "content": results})
        root["status"] = "step_limit"
        return "Stopped: step limit reached."


def summary(path: str) -> None:
    spans = [json.loads(line) for line in open(path)]
    llm = [s for s in spans if s["name"] == "llm"]
    tools = [s for s in spans if s["name"] == "tool"]
    roots = [s for s in spans if s["name"] == "interaction"]
    print(f"\n{len(roots)} interactions | {len(llm)} llm calls | {len(tools)} tool calls")
    print(f"tokens in {sum(s['input_tokens'] for s in llm)}  out {sum(s['output_tokens'] for s in llm)}  "
          f"cost ${sum(s['cost_usd'] for s in llm):.5f}")
    durations = sorted(s["duration_ms"] for s in roots)
    print(f"interaction latency: median {durations[len(durations) // 2]} ms, worst {durations[-1]} ms")
    print(f"errors: {sum(s['status'] != 'ok' for s in spans)}")


_mock_turn = {"n": 0}


def mock_responder(kw: dict):
    # Alternate: first ask for the tool, then answer from its result.
    last = kw["messages"][-1]["content"]
    if isinstance(last, list) and last and last[0].get("type") == "tool_result":
        return "The contract ends on the date shown in the lookup result."
    _mock_turn["n"] += 1
    return [{"type": "tool_use", "id": f"toolu_{_mock_turn['n']}", "name": "check_contract_status",
             "input": {"vendor_name": "Nimbus Cloud Services"}}]


if __name__ == "__main__":
    client = get_client(mock_responder, latency=0.1)
    tracer = Tracer(TRACE_FILE)
    for q in ["When does the Nimbus Cloud Services contract end?", "Does Nimbus auto-renew?"]:
        print(traced_agent(client, tracer, q))
    summary(TRACE_FILE)
    print(f"Spans written to {TRACE_FILE}")
