"""Lab 3 (Module 3): a complete prompt-evaluation harness.

What it shows
1. Structured outputs: the answer must match a JSON schema (output_config.format).
2. Ground truth computed in code (contracts.expected), not typed by hand.
3. Two graders: an exact code grader for fields, and a model grader for the written reason.
4. A pass-rate report and a non-zero exit code, so the eval can gate CI.

Run
    python lab03_eval_harness.py --mock          # offline: one case is deliberately wrong
    python lab03_eval_harness.py                 # live, needs ANTHROPIC_API_KEY
    python lab03_eval_harness.py --threshold 1.0 # fail unless every case passes

Exercise: change PROMPT_VERSION's wording (for example remove the risk rule) and rerun.
Which cases fail, and does the code grader or the model grader catch it?
"""
from __future__ import annotations

import argparse
import json

from common import HAIKU, SONNET, TODAY, get_client, json_of, last_user_text
from contracts import CONTRACTS, RISK_RULE, describe, expected, find

PROMPT_VERSION = "v2"

SYSTEM = f"""You are a contract renewal analyst. Today is {TODAY}.
{RISK_RULE}
Return only the JSON object the schema asks for. In "reason", show the date arithmetic in one sentence."""

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string"},
        "cancellation_deadline": {"type": ["string", "null"], "description": "YYYY-MM-DD, or null if it does not auto-renew"},
        "days_until_deadline": {"type": ["integer", "null"]},
        "risk": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
        "reason": {"type": "string"},
    },
    "required": ["vendor", "cancellation_deadline", "days_until_deadline", "risk", "reason"],
    "additionalProperties": False,
}

GRADE_SCHEMA = {
    "type": "object",
    "properties": {"verdict": {"type": "string", "enum": ["PASS", "FAIL"]}, "why": {"type": "string"}},
    "required": ["verdict", "why"],
    "additionalProperties": False,
}


def classify(client, contract: dict) -> dict:
    resp = client.messages.create(
        model=SONNET,
        max_tokens=600,
        system=SYSTEM,
        output_config={"format": {"type": "json_schema", "schema": ANSWER_SCHEMA}, "effort": "low"},
        messages=[{"role": "user", "content": f"<contract>{describe(contract)}</contract>"}],
    )
    return json_of(resp)


def code_grade(answer: dict, truth: dict) -> list[str]:
    """Exact comparison of the fields that have one right answer."""
    errors = []
    for field in ("cancellation_deadline", "days_until_deadline", "risk"):
        if answer.get(field) != truth[field]:
            errors.append(f"{field}: got {answer.get(field)!r}, expected {truth[field]!r}")
    return errors


def model_grade(client, contract: dict, answer: dict) -> dict:
    """A cheaper model checks whether the written reason is consistent with the rule."""
    resp = client.messages.create(
        model=HAIKU,
        max_tokens=300,
        output_config={"format": {"type": "json_schema", "schema": GRADE_SCHEMA}},
        messages=[{"role": "user", "content": (
            f"Today is {TODAY}.\n{RISK_RULE}\n\n<contract>{describe(contract)}</contract>\n"
            f"<answer>{json.dumps(answer)}</answer>\n"
            "Grade PASS only if the reason's arithmetic is correct AND the risk follows the rule.")}],
    )
    return json_of(resp)


# ------------------------------------------------------------- offline mock
def mock_responder(kw: dict):
    text = last_user_text(kw)
    contract = find(text)
    if "<answer>" in text:  # grader call
        answer = json.loads(text.split("<answer>")[1].split("</answer>")[0])
        ok = not code_grade(answer, expected(contract))
        return json.dumps({"verdict": "PASS" if ok else "FAIL", "why": "arithmetic checked"})
    truth = dict(expected(contract))
    if contract["vendor"].startswith("Vertex"):  # a planted mistake so the graders have something to catch
        truth["risk"] = "LOW"
    truth["reason"] = f"Deadline {truth['cancellation_deadline']} is {truth['days_until_deadline']} days from {TODAY}."
    return json.dumps(truth)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.8)
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    client = get_client(mock_responder)
    results = []
    print(f"Prompt {PROMPT_VERSION} | {len(CONTRACTS)} cases\n")
    print(f"{'vendor':32} {'risk':7} {'code':5} {'model':5}")
    for c in CONTRACTS:
        answer = classify(client, c)
        errors = code_grade(answer, expected(c))
        verdict = model_grade(client, c, answer)["verdict"]
        passed = not errors and verdict == "PASS"
        results.append(passed)
        print(f"{c['vendor']:32} {answer['risk']:7} {'ok' if not errors else 'FAIL':5} {verdict:5}")
        for e in errors:
            print(f"    - {e}")

    rate = sum(results) / len(results)
    print(f"\nPass rate {rate:.0%} (threshold {args.threshold:.0%})")
    return 0 if rate >= args.threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
