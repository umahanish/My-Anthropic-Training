# Python Labs 2026: Building with Claude

Hands-on code for the 10-module Claude course, updated for the Claude 5.5 model family.
Every lab runs **offline with `--mock`**, so participants can study the code path before API keys
are provisioned, and runs **live** once `ANTHROPIC_API_KEY` is set.

## Setup (10 minutes, do it before Day 1)

```bash
git clone https://github.com/umahanish/My-Anthropic-Training.git
cd My-Anthropic-Training/Training/Python-Labs-2026
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env               # never commit this file
python lab03_eval_harness.py --mock                      # smoke test: should print a pass-rate table
```

## Lab map

| Module | File | What participants build | Key needed |
|---|---|---|---|
| 3 Prompting & evals | `lab03_eval_harness.py` | Structured outputs, code-computed answer key, code grader + model grader, CI exit code | live or `--mock` |
| 4 Claude API | `lab04_tool_loop.py` | A complete tool-use loop with a step cap | live or `--mock` |
| 4 Claude API | `lab04_caching_effort_strict_tools.py` | Prompt caching (cache write vs read), effort low vs high, strict tools replacing forced tool use | live or `--mock` |
| 5 RAG | `lab05_hybrid_search.py` | BM25 and reciprocal rank fusion on a toy set | none |
| 5 RAG | `lab05_rag_end_to_end.py` | Load the real contract .docx files, chunk with context headers, retrieval eval, grounded answer with citations | eval: none; ask: live or `--mock` |
| 6 MCP | `lab06_contract_server.py` | A FastMCP server with a tool and a resource | none (`--test`) |
| 6 MCP | `lab06_mcp_security.py` | Least privilege, schema-enforced validation, untrusted-content flagging, audit log | none (`--test`) |
| 8 Agents | `lab08_router.py` | Route simple questions to Haiku, complex ones to Sonnet | live or `--mock` |
| 8 Agents | `lab08_parallel_orchestrator.py` | Orchestrator plan (JSON) -> code gate -> parallel Haiku workers -> synthesis, with a cost report | live or `--mock` |
| 9 Enterprise | `lab09_model_benchmark.py` | Accuracy, latency and monthly cost per model on the same graded task | live or `--mock` |
| 9 Enterprise | `lab09_skill_scanner.py` | Static review of Skills and plugins for exfiltration, secrets access, injection, broad permissions | none |
| 10 Operations | `lab10_tracing.py` | Span tracing for your own agent, redacted by default, with a cost and latency summary | live or `--mock` |
| 10 Operations | `lab10_regression_gate.py` + `ci_example.yml` | Baseline the eval score and fail CI when it drops | live or `--mock` |
| 10 Operations | `lab10_guardrails_and_evals.py` | Input, output and tool-allowlist guardrails with negative test cases | none |

Shared files: `common.py` (client, model IDs, prices, mock client) and `contracts.py` (the five course
contracts and the risk rule every lab is graded against).

## API rules for the 5.5 models

Each of these returns HTTP 400 on `claude-sonnet-5-5` and `claude-opus-5-5`; the labs are written to avoid them:

- `temperature`, `top_p`, `top_k` set to non-default values. Control depth with `output_config={"effort": "low" | "medium" | "high"}`.
- `thinking={"type": "disabled"}` or thinking budgets.
- Forced tool use: `tool_choice` of `any` or `tool`. Use `auto` with `"strict": true` tools.
- Assistant prefill. Use structured outputs (`output_config.format`) for fixed JSON.

Check the model's "What's new" page on docs.claude.com before changing model versions.

## Facilitator notes

- Run every lab once with `--mock` the day before, and once live with the cohort's keys.
- Live labs spend a few cents each; `lab09_model_benchmark.py` calls Opus and costs the most.
- Prices in `common.PRICES` are for the cost reports only. Verify them on the pricing page before quoting.
- Discussion prompts and exercises are in each file's docstring.
- `lab06_mcp_security.py` teaching point: rejected calls fail schema validation before reaching the tool, so
  they never appear in the tool's own audit log. Ask the group where production logging should sit instead.
