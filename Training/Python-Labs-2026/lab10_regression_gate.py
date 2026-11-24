"""Lab 10b (Module 10): an eval regression gate for CI.

Runs the Lab 3 eval harness, compares the pass rate with a stored baseline, and exits non-zero
if quality dropped. Wire it into CI (see ci_example.yml) so a prompt or model change that breaks
a working case fails the build, like a failing unit test.

Run
    python lab10_regression_gate.py --mock --update-baseline   # record today's score as the baseline
    python lab10_regression_gate.py --mock                      # compare against it

Exercise: record a baseline, then make quality drop and rerun. Offline: in lab03's mock_responder,
plant a second mistake (for example also mis-grade Alderwood). Live: change the model in
lab03.classify from SONNET to HAIKU, or weaken the system prompt. Watch the gate fail with exit 1.
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import lab03_eval_harness as harness

BASELINE = Path(__file__).with_name("eval_baseline.json")
TOLERANCE = 0.0  # allowed drop in pass rate before the gate fails


def score() -> float:
    sys.argv = [sys.argv[0], "--threshold", "0"] + (["--mock"] if "--mock" in sys.argv else [])
    out = io.StringIO()
    with redirect_stdout(out):
        harness.main()
    line = next(l for l in out.getvalue().splitlines() if l.startswith("Pass rate"))
    print(out.getvalue())
    return float(line.split()[2].rstrip("%")) / 100


if __name__ == "__main__":
    update = "--update-baseline" in sys.argv
    rate = score()
    if update or not BASELINE.exists():
        BASELINE.write_text(json.dumps({"pass_rate": rate, "prompt_version": harness.PROMPT_VERSION}))
        print(f"Baseline recorded: {rate:.0%}")
        raise SystemExit(0)
    base = json.loads(BASELINE.read_text())["pass_rate"]
    if rate + TOLERANCE < base:
        print(f"REGRESSION: pass rate {rate:.0%} is below baseline {base:.0%}. Failing the build.")
        raise SystemExit(1)
    print(f"OK: pass rate {rate:.0%} (baseline {base:.0%})")
