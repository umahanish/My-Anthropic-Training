"""Lab 8b (Module 8): orchestrator-workers with real parallelism, a gate, and a cost report.

Flow
    1. Orchestrator (Sonnet) reads the task and returns a plan as JSON (structured output).
    2. Gate (plain code) rejects any subtask that names a contract we do not have.
    3. Workers (Haiku) run concurrently with asyncio.gather, capped by a semaphore.
    4. Each worker result is checked against the code-computed answer key.
    5. Synthesiser (Sonnet) writes the final prioritised action list.

Run
    python lab08_parallel_orchestrator.py --mock     # offline; shows the parallel speed-up
    python lab08_parallel_orchestrator.py            # live

Exercise: set MAX_CONCURRENCY = 1 and compare wall time. Then add a sixth, made-up vendor
to TASK and confirm the gate stops it before any worker spends tokens on it.
"""
from __future__ import annotations

import asyncio
import json
import time

from common import HAIKU, SONNET, TODAY, cost_usd, get_async_client, json_of, last_user_text, text_of
from contracts import CONTRACTS, RISK_RULE, describe, expected, find

MAX_CONCURRENCY = 5
TASK = "Assess renewal risk for every vendor contract we hold and tell me what to do this month."

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "subtasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"vendor": {"type": "string"}, "instruction": {"type": "string"}},
                "required": ["vendor", "instruction"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["subtasks"],
    "additionalProperties": False,
}

WORKER_SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string"},
        "risk": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
        "action": {"type": "string"},
    },
    "required": ["vendor", "risk", "action"],
    "additionalProperties": False,
}

spend = {"tokens_in": 0, "tokens_out": 0, "usd": 0.0}


def track(model: str, resp) -> None:
    spend["tokens_in"] += resp.usage.input_tokens
    spend["tokens_out"] += resp.usage.output_tokens
    spend["usd"] += cost_usd(model, resp.usage.input_tokens, resp.usage.output_tokens)


async def plan(client) -> list[dict]:
    inventory = "\n".join(describe(c) for c in CONTRACTS)
    resp = await client.messages.create(
        model=SONNET, max_tokens=1200,
        output_config={"format": {"type": "json_schema", "schema": PLAN_SCHEMA}, "effort": "low"},
        messages=[{"role": "user", "content": f"Task: {TASK}\n<inventory>\n{inventory}\n</inventory>\n"
                   "Split the task into one subtask per contract that needs assessment."}],
    )
    track(SONNET, resp)
    return json_of(resp)["subtasks"]


def gate(subtasks: list[dict]) -> list[dict]:
    known = {c["vendor"] for c in CONTRACTS}
    passed = [s for s in subtasks if s["vendor"] in known]
    for s in subtasks:
        if s["vendor"] not in known:
            print(f"  gate: dropped unknown vendor {s['vendor']!r}")
    return passed


async def worker(client, sem: asyncio.Semaphore, subtask: dict) -> dict:
    contract = next(c for c in CONTRACTS if c["vendor"] == subtask["vendor"])
    async with sem:
        t0 = time.perf_counter()
        resp = await client.messages.create(
            model=HAIKU, max_tokens=400,
            system=f"Today is {TODAY}.\n{RISK_RULE}",
            output_config={"format": {"type": "json_schema", "schema": WORKER_SCHEMA}},
            messages=[{"role": "user", "content": f"{subtask['instruction']}\n<contract>{describe(contract)}</contract>"}],
        )
    track(HAIKU, resp)
    result = json_of(resp)
    result["correct"] = result["risk"] == expected(contract)["risk"]
    result["seconds"] = round(time.perf_counter() - t0, 2)
    return result


async def synthesise(client, results: list[dict]) -> str:
    resp = await client.messages.create(
        model=SONNET, max_tokens=800, output_config={"effort": "low"},
        messages=[{"role": "user", "content": "Write a prioritised action list (HIGH first) from these assessments:\n"
                   + json.dumps(results, indent=1)}],
    )
    track(SONNET, resp)
    return text_of(resp)


async def main() -> None:
    client = get_async_client(mock_responder)
    t0 = time.perf_counter()
    subtasks = gate(await plan(client))
    print(f"Plan: {len(subtasks)} subtasks after the gate")

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    t_workers = time.perf_counter()
    results = await asyncio.gather(*(worker(client, sem, s) for s in subtasks))
    wall = time.perf_counter() - t_workers
    serial = sum(r["seconds"] for r in results)

    for r in results:
        print(f"  {r['vendor']:32} {r['risk']:7} {'ok' if r['correct'] else 'WRONG'}  {r['seconds']}s")
    print(f"Workers: {wall:.2f}s wall vs {serial:.2f}s if run one by one (concurrency {MAX_CONCURRENCY})")

    print("\n" + await synthesise(client, results))
    print(f"\nTotal {time.perf_counter() - t0:.2f}s | tokens in {spend['tokens_in']} out {spend['tokens_out']} | ${spend['usd']:.4f}")


def mock_responder(kw: dict):
    text = last_user_text(kw)
    if "<inventory>" in text:
        return json.dumps({"subtasks": [{"vendor": c["vendor"], "instruction": "Classify renewal risk and give one action."} for c in CONTRACTS]
                           + [{"vendor": "Imaginary Vendor Ltd", "instruction": "Classify renewal risk."}]})
    if "<contract>" in text:
        c = find(text)
        return json.dumps({"vendor": c["vendor"], "risk": expected(c)["risk"], "action": "Review with the owning team."})
    return "1. Cancel or renegotiate HIGH-risk renewals before their deadlines.\n2. Schedule MEDIUM reviews.\n3. Monitor LOW."


if __name__ == "__main__":
    asyncio.run(main())
