"""Lab 9a (Module 9): choose a model with data, not opinion.

Runs the same graded task on Haiku, Sonnet and Opus and reports accuracy, latency and cost,
then projects the monthly bill for a given volume. The answer key comes from contracts.expected.

Run
    python lab09_model_benchmark.py --mock
    python lab09_model_benchmark.py --volume 50000      # live; 50k classifications a month

Discussion: which model is the cheapest one that still meets your accuracy bar?
Write that rule down; it is your routing policy for Module 8's router.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import time

from common import HAIKU, OPUS, SONNET, TODAY, cost_usd, get_client, json_of, last_user_text
from contracts import CONTRACTS, RISK_RULE, describe, expected, find

SCHEMA = {
    "type": "object",
    "properties": {"risk": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]}},
    "required": ["risk"],
    "additionalProperties": False,
}


def run(client, model: str) -> dict:
    correct, latencies, costs = 0, [], []
    for c in CONTRACTS:
        t0 = time.perf_counter()
        resp = client.messages.create(
            model=model, max_tokens=1000,
            system=f"Today is {TODAY}.\n{RISK_RULE}",
            output_config={"format": {"type": "json_schema", "schema": SCHEMA}, "effort": "low"},
            messages=[{"role": "user", "content": f"<contract>{describe(c)}</contract>"}],
        )
        latencies.append(time.perf_counter() - t0)
        costs.append(cost_usd(model, resp.usage.input_tokens, resp.usage.output_tokens))
        correct += json_of(resp)["risk"] == expected(c)["risk"]
    return {
        "model": model,
        "accuracy": correct / len(CONTRACTS),
        "p50_s": statistics.median(latencies),
        "max_s": max(latencies),
        "usd_per_call": statistics.mean(costs),
    }


def mock_responder(kw: dict):
    c = find(last_user_text(kw))
    risk = expected(c)["risk"]
    if kw["model"] == HAIKU and c["vendor"].startswith("Vertex"):
        risk = "HIGH"  # simulate the smaller model slipping on the boundary case
    return json.dumps({"risk": risk})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=10_000, help="calls per month for the cost projection")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    client = get_client(mock_responder, latency=0.05)
    rows = [run(client, m) for m in (HAIKU, SONNET, OPUS)]
    print(f"{'model':20} {'accuracy':>8} {'p50 s':>6} {'max s':>6} {'$/call':>9} {'$/month':>9}")
    for r in rows:
        r["usd_per_month"] = r["usd_per_call"] * args.volume
        print(f"{r['model']:20} {r['accuracy']:>8.0%} {r['p50_s']:>6.2f} {r['max_s']:>6.2f} "
              f"{r['usd_per_call']:>9.5f} {r['usd_per_month']:>9.2f}")
    with open("model_benchmark.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("\nSaved model_benchmark.csv. Prices come from common.PRICES; verify them on the pricing page.")
