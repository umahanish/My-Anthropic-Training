# Classic MCP vs Code Mode: live demo

**Classic MCP:** the LLM sees every tool definition and calls tools one at a time. Every tool result, however large, goes back through the model before the next step.

**Code Mode** ([UTCP `code-mode`](https://github.com/universal-tool-calling-protocol/code-mode)): the LLM sees **one** tool, `call_tool_chain`. It writes code, in TypeScript or Python, and a sandbox runs it with the MCP tools available as plain functions. Loops, filtering, and decisions happen in code, and only the small final result goes back to the model.

All demos use the **same real MCP server**, the same Claude model (`claude-sonnet-5-5`), and the same task.

## Files
| File | What it is |
|---|---|
| `travel_server.py` | One MCP server (stdio, Python `mcp==2.3.0`): `list_offices`, `get_weather` (returns a 24-hour forecast, like real APIs), `book_flight` |
| `demo1_classic.py` | Demo 1: Claude plus MCP tools, called one by one |
| `demo2_codemode.mjs` | Demo 2a: Code Mode in **TypeScript** (`@utcp/code-mode` + `@utcp/mcp`) |
| `demo2_codemode.py` | Demo 2b: Code Mode in **Python** (`code-mode` + `utcp-mcp`) |

## Setup
```bash
git clone https://github.com/manojkanur/mcp-vs-code-mode.git && cd mcp-vs-code-mode
```
```bash
uv venv .venv && uv pip install -p .venv "mcp==2.3.0" anthropic                    # classic demo
uv venv .venv-codemode && uv pip install -p .venv-codemode code-mode utcp utcp-mcp anthropic   # Python Code Mode
npm install                                                                         # TypeScript Code Mode
```
Python Code Mode gets its own venv because `utcp-mcp` requires `mcp<2`, which conflicts with the `mcp==2.3.0` the classic demo uses.

## Run (in each new terminal)
```bash
cd mcp-vs-code-mode
export ANTHROPIC_API_KEY='your-key'

.venv/bin/python demo1_classic.py              # Demo 1: Classic MCP
node demo2_codemode.mjs                        # Demo 2a: Code Mode (TypeScript)
.venv-codemode/bin/python demo2_codemode.py    # Demo 2b: Code Mode (Python)
```
You don't need to start the MCP server: each demo launches `travel_server.py` itself.

## Step-by-step demo

### Step 1: Show the MCP server
Open `travel_server.py`. It has three `@mcp.tool()` functions with typed return values. `get_weather` returns about 1.3 KB of hourly forecast per city.

### Step 2: Classic MCP
```
  [LLM turn 1] Claude -> MCP list_offices({}) => {"offices":["Chennai", ... "Dubai"]}
  [LLM turn 2] Claude -> MCP get_weather({'city': 'Chennai'}) => {...} (1289 chars sent to Claude)
  ... 7 more cities, every forecast pushed into Claude's context ...
  [LLM turn 3] Claude -> MCP book_flight({'destination': 'Dubai', 'date': '2026-11-20'}) => PNR-DUB42
STATS  LLM calls=4  MCP tool calls=10  input tokens=16724  output tokens=786  time=9.2s
```

### Step 3a: Code Mode in TypeScript
```
STEP 4: Claude wrote this code:
    | const o = travel.travel_list_offices({});
    | const ws = [];
    | for (const c of o.offices) { try { ws.push(travel.travel_get_weather({city:c})); } catch(e) { ... } }
    | return ws.map(w=>({city:w.city,temp:w.temp_c,cond:w.condition}));
  [sandbox -> MCP] ... 9 calls, all inside the sandbox ...
STEP 4: Claude wrote this code:
    | return travel.travel_book_flight({destination:"Dubai", date:"2026-11-20"});
STATS  LLM calls=3  MCP tool calls=10  input tokens=6709  output tokens=522  time=6.3s
```

### Step 3b: Code Mode in Python (the whole task in one code run)
```
STEP 4: Claude wrote this code:
    | offices = travel.list_offices()["offices"]
    | res = []
    | for c in offices:
    |     w = travel.get_weather(city=c)
    |     res.append((c, w["temp_c"], w["condition"]))
    | ok = [r for r in res if not any(k in r[2].lower() for k in ["rain","storm","thunder","shower","drizzle"])]
    | best = max(ok, key=lambda r: r[1])
    | b = travel.book_flight(destination=best[0], date="2026-11-20")
    | return {"all": res, "best": best, "booking": b}
  [sandbox -> MCP] travel.list_offices({})  ... 8 x get_weather ...  travel.book_flight(Dubai)
STATS  LLM calls=2  MCP tool calls=10  input tokens=4268  output tokens=531  time=5.7s
```

### Step 4: Compare
| | Classic MCP | Code Mode (TS) | Code Mode (Python) |
|---|---|---|---|
| Tools the LLM sees | 3 definitions | 1 tool + TS interfaces | 1 tool + Python TypedDicts |
| LLM calls | 4 | 3 | **2** |
| Input tokens | 16,724 | 6,709 (−60%) | **4,268 (−74%)** |
| Time | 9.2 s | 6.3 s | 5.7 s |
| Answer | Dubai, PNR-DUB42 | Dubai, PNR-DUB42 | Dubai, PNR-DUB42 |

These are single runs. LLM output varies, so whether Claude books inside the same code run (2 calls) or in a second step (3 calls) changes from run to run in both languages.

## TypeScript vs Python Code Mode
| | TypeScript | Python |
|---|---|---|
| Package | `@utcp/code-mode` 1.2.13 | `code-mode` 1.1.0 |
| Sandbox | `isolated-vm` (separate V8 isolate, memory and time limits) | `RestrictedPython` (restricts code, weaker isolation) |
| Worked out of the box | Yes | **No.** Needed 4 fixes (below) |

**Python fixes**, all in the `CodeMode` subclass at the top of `demo2_codemode.py` (the library itself is unmodified):
1. `code-mode` 1.1.0 doesn't implement `close()`, which `utcp` 1.2 made abstract, so the client can't be created.
2. Tool calls from sandboxed code ran on a new event loop while the MCP connection lived on the main one, so every call **hung forever**. The fix sends calls back to the main loop.
3. RestrictedPython's standard guards weren't set, so any `for` loop or `d["key"]` failed. The fix adds RestrictedPython's own default guards.
4. `any`, `all`, `list`, `dict`, and `set` were missing from the sandbox's built-ins.

Separately, `utcp-mcp` crashes on MCP tools that have no output schema. Typed return values in `travel_server.py` avoid that, and they also give both Code Mode versions better generated interfaces.

## What to tell the audience
- **Code Mode does not replace MCP; it sits on top of it.** The same MCP server runs unchanged. Code Mode is an MCP client that exposes the tools as functions in code.
- **The win grows with data size and step count.** Each extra tool result costs classic MCP more context, while Code Mode returns only what the code chooses to.
- **Trade-offs:**
  - You have to run a code sandbox.
  - The model has to write correct code. In TypeScript, Claude sometimes called `.then()` on tool results, so the demo prompt includes one line about it.
  - The ecosystem is young, especially the Python package.

## Bonus: Code Mode as an MCP server
Any MCP client (Claude Desktop, Claude Code) can use Code Mode directly:
```json
{ "mcpServers": { "code-mode": { "command": "npx", "args": ["@utcp/code-mode-mcp"],
    "env": { "UTCP_CONFIG_FILE": "/path/to/.utcp_config.json" } } } }
```
