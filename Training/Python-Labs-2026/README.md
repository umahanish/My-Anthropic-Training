# Python labs (2026, Claude 5.5 family)

Setup:

    pip install anthropic python-dotenv rank-bm25 fastmcp
    echo "ANTHROPIC_API_KEY=sk-ant-..." > .env   # never commit this file

| File | Lab | Needs API key |
|---|---|---|
| common.py | Shared client, model IDs, response helper | - |
| lab04_tool_loop.py | Tool-use loop with a step cap | yes |
| lab05_hybrid_search.py | BM25 + reciprocal rank fusion | no |
| lab06_contract_server.py | MCP server (`--test` runs offline) | no |
| lab08_router.py | Route simple vs complex questions | yes |
| lab10_guardrails_and_evals.py | Input guardrails and regression cases | no |

API rules for the 5.5 models: do not set `temperature`, `top_p` or `top_k`, and do not disable thinking. Model IDs: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5.

Offline tests run without a key: `python lab05_hybrid_search.py`, `python lab10_guardrails_and_evals.py`, `python lab06_contract_server.py --test`.
Live labs were syntax-checked; run them with a key before the session.
