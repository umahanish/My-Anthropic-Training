# The Claude API In Depth — Student Lab Guide
### Module 4: From Messages to Multi-Tool Agents

This is your copy — basic theory plus labs, building directly on Module 3. Same Console account, same Workbench, same `pip install anthropic` setup — if any of that isn't working yet, sort it out before Lab 4.1.

**Legend:** 🟢 Core (Workbench, minimal/no code) · 🔵 Stretch (real Python scripts)

**One thing that changed since Module 3:** several labs below need real Python, not just the Workbench — tool-use loops, file uploads, and context management all require your own code to complete the round trip. Where that's true, the Core lab teaches the concept in the Workbench and the Stretch lab completes it in code.

---

## 1. API Architecture: Models, Endpoints & Authentication

**Basic theory:**
- The Claude API is a REST API at `https://api.anthropic.com`. The endpoint you'll use almost always is `POST /v1/messages`.
- Every request needs three headers: `x-api-key` (your key), `anthropic-version` (a date string, e.g. `2023-06-01`), and `content-type: application/json`. The Python/TypeScript SDKs send these for you automatically once you set `ANTHROPIC_API_KEY`.
- Current model names you'll see today: `claude-opus-5` (most capable), `claude-sonnet-5` (balanced — what today's labs use), `claude-haiku-4-5-20251001` (fastest/cheapest).
- API keys start with `sk-ant-` and are shown in full only once, at creation — store it somewhere safe immediately.

### 🟢 Lab 1.1 — Your First Raw Request *(10 min)*
1. In the Workbench, build this exact request in **Form** view:
   - System prompt: leave empty
   - User message: `What should I check first when a vendor contract is about to auto-renew?`
2. Click **Run**, then click the **Code** toggle at the top of the request panel.
3. Look at the generated snippet — that `x-api-key` / `anthropic-version` / `content-type` header trio is present even though you never typed it. That's the whole authentication story for direct HTTP calls.

### 🔵 Lab 1.2 (Stretch) — The Same Call, Raw curl *(10 min)*
1. In a terminal, run (swap in your real key or export it first):
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "content-type: application/json" \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -d '{
       "model": "claude-sonnet-5",
       "max_tokens": 300,
       "messages": [{"role": "user", "content": "What should I check first when a vendor contract is about to auto-renew?"}]
     }'
   ```
2. Compare the raw JSON response to what the Workbench showed you — same shape, no SDK in between.

---

## 2. Multi-Turn Conversations & Context Windows

**Basic theory:**
- The Messages API is **stateless** — Claude has no memory of past requests. Every turn, you resend the *entire* conversation history yourself.
- Messages must strictly alternate `user` → `assistant` → `user`, starting with `user`. You build this up as a growing list.
- The system prompt is a **separate top-level parameter**, not a message — it's not part of the alternating history.
- Context window: standard 200K tokens, up to 1M on some models. Everything counts toward it — system prompt, every message, tool definitions, and Claude's own output.

### 🟢 Lab 2.1 — Watch Statelessness Happen *(10 min)*
1. In the Workbench, send: `My name is Priya and I work on the Nimbus migration project. Remember that.`
2. Click **Reset** (or open a brand new request) and, in a *fresh* request with no history, ask: `What's my name and what project am I working on?`
3. Claude won't know — there's nothing to know, because nothing was actually stored anywhere. This is the single most important mental model shift from using claude.ai (which handles history for you) to using the raw API (which doesn't).

### 🔵 Lab 2.2 (Stretch) — Build the History Yourself *(15 min)*
1. Save as `multiturn.py`:
   ```python
   from anthropic import Anthropic

   client = Anthropic()
   messages = []

   def ask(user_text):
       messages.append({"role": "user", "content": user_text})
       response = client.messages.create(
           model="claude-sonnet-5",
           max_tokens=300,
           messages=messages,
       )
       reply = next(b.text for b in response.content if b.type == "text")
       messages.append({"role": "assistant", "content": reply})
       print(f"Claude: {reply}\n")

   ask("My name is Priya and I work on the Nimbus migration project. Remember that.")
   ask("What's my name and what project am I working on?")
   ```
2. Run it: `python multiturn.py`. This time it remembers — because *your code*, not Claude, is carrying the history forward on the second call.

---

## 3. Temperature, Streaming & Response Formatting

**Basic theory:**
- `temperature` ranges 0.0–1.0 (default 1.0). Lower = more focused/deterministic, higher = more varied. Even at 0.0, output isn't perfectly identical every time.
- `stream: true` switches a request from "wait for the whole answer" to a live feed of Server-Sent Events — useful for anything a human is watching in real time.
- Every response has a `stop_reason` (`end_turn`, `max_tokens`, `tool_use`, or `stop_sequence`) — always check this before assuming Claude finished naturally.

### 🟢 Lab 3.1 — Temperature, Side by Side *(10 min)*
1. In the Workbench, open model settings and set **temperature to 0**. Ask: `Suggest a one-line subject for an email about a contract renewal deadline.` Run it 3 times.
2. Set **temperature to 1**. Run the same prompt 3 times.
3. Compare: the temperature-0 runs should read as near-identical; the temperature-1 runs should vary more in phrasing.

### 🔵 Lab 3.2 (Stretch) — Streaming in Code *(12 min)*
1. Save as `stream_demo.py`:
   ```python
   from anthropic import Anthropic

   client = Anthropic()

   with client.messages.stream(
       model="claude-sonnet-5",
       max_tokens=300,
       messages=[{"role": "user", "content": "List 3 things to check before a contract auto-renews."}],
   ) as stream:
       for text in stream.text_stream:
           print(text, end="", flush=True)
       print()
       final = stream.get_final_message()
       print(f"\n\nstop_reason: {final.stop_reason}")
   ```
2. Run it: `python stream_demo.py`. Watch the text appear incrementally instead of all at once, then check the printed `stop_reason` at the end.

---

## 4. Tool Use: Schemas, Message Blocks & Multi-Turn Tools

**Basic theory:**
- A **tool** is a function you describe to Claude with a `name`, a `description`, and an `input_schema` (JSON Schema). Claude never runs your code — it only ever tells you *what* it wants to call and *with what arguments*.
- When Claude wants to use one, the response has `stop_reason: "tool_use"` and a `tool_use` content block with `name`, `id`, and `input`.
- You run the real function yourself, then send the result back as a `tool_result` block in a new **user** message — it must reference the same `id` and come immediately after, with nothing in between.
- ⚠️ **Two valid shapes, depending on the layer.** SDK code (Python/TypeScript) uses the flat form: `{"name":, "description":, "input_schema":}`. The raw wire format wraps it as `{"type": "custom", "custom": {"name":, "description":, "input_schema":}}`. You'll never type that wrapper by hand, though — in both the SDK and the Workbench's Add Tool dialog, you fill in Name, Description, and Input Schema as separate fields, and the wrapper gets assembled underneath automatically.

### 🟢 Lab 4.1 — Define a Tool, See It Fire *(12 min)*
1. In the Workbench, click **Add** → **Tools** → **Custom Tool**. You'll get three separate fields — Name, Description, and Input Schema. Fill in each one directly; don't paste a combined JSON block across all three, the dialog builds the full tool definition from these fields itself:
   - **Name:**
     ```
     check_contract_status
     ```
   - **Description:**
     ```
     Look up the renewal status of a vendor contract by vendor name.
     ```
   - **Input Schema** (schema only — no `name`, `description`, or wrapper here, just the JSON Schema object itself):
     ```json
     {
       "type": "object",
       "properties": {
         "vendor_name": { "type": "string", "description": "The vendor's name" }
       },
       "required": ["vendor_name"]
     }
     ```
2. **Add tool** stays greyed out until all three fields above are actually filled in (placeholder text like "tool_name" doesn't count) *and* the Input Schema box contains a complete, correctly-closed JSON object. A fast self-check: count the closing `}` at the very end of the box against what the shape above should have — one extra brace almost always means leftover content from an earlier paste wasn't fully cleared.
3. Once **Add tool** is clickable, click it, then ask: `What's the renewal status of the Nimbus Cloud Services contract?`
4. Claude won't answer directly — the response will show a **Tool Call**: `check_contract_status({"vendor_name": "Nimbus Cloud Services"})`. That's the whole mechanism working: Claude read the question, recognized it needed data it doesn't have, and requested the tool instead of guessing.
5. This is a *request*, not a finished answer — the Workbench has no code behind it to actually run `check_contract_status` and hand back a result, so the exchange stops here. Completing it is exactly what Lab 4.2 does in real code. *(Optional to explore first: the wrench icon and "Add to Conversation" button near the tool call may let you manually supply a fake result and continue right there in the Workbench — worth poking at before moving to Lab 4.2, though confirm what it actually does rather than assume.)*

### 🔵 Lab 4.2 (Stretch) — Complete the Loop in Code *(20 min)*
This picks up exactly where Lab 4.1 stopped — Claude requesting the tool call but nothing actually answering it. Here, your code plays the missing piece: receive the request, run the real function, send back a result.
1. Save as `tool_loop.py`:
   ```python
   from anthropic import Anthropic

   client = Anthropic()

   # Pretend "database" standing in for your 5 course contracts
   CONTRACTS = {
       "nimbus cloud services": "Auto-renews Sept 25, 2026 unless cancelled by Aug 26.",
       "brightpath security solutions": "Auto-renews Oct 10, 2026 unless cancelled by Aug 26.",
   }

   def check_contract_status(vendor_name: str) -> str:
       return CONTRACTS.get(vendor_name.lower(), "No record found for that vendor.")

   tools = [{
       "name": "check_contract_status",
       "description": "Look up the renewal status of a vendor contract by vendor name.",
       "input_schema": {
           "type": "object",
           "properties": {"vendor_name": {"type": "string"}},
           "required": ["vendor_name"],
       },
   }]

   messages = [{"role": "user", "content": "What's the renewal status of the Nimbus Cloud Services contract?"}]

   response = client.messages.create(
       model="claude-sonnet-5", max_tokens=500, tools=tools, messages=messages,
   )
   messages.append({"role": "assistant", "content": response.content})

   if response.stop_reason == "tool_use":
       tool_block = next(b for b in response.content if b.type == "tool_use")
       result = check_contract_status(**tool_block.input)
       messages.append({
           "role": "user",
           "content": [{"type": "tool_result", "tool_use_id": tool_block.id, "content": result}],
       })
       final = client.messages.create(model="claude-sonnet-5", max_tokens=500, tools=tools, messages=messages)
       print(next(b.text for b in final.content if b.type == "text"))
   ```
2. Run it: `python tool_loop.py`. This is Lab 4.1's mechanism, completed end to end — Claude asks, your code answers, Claude replies to the human using your real data.

---

## 5. Advanced Tool Patterns: Multiple Tools & Fine-Grained Control

**Basic theory:**
- `tool_choice` controls how much freedom Claude has: `{"type": "auto"}` (default, Claude decides), `{"type": "any"}` (must use *some* tool), `{"type": "tool", "name": "..."}` (must use *this specific* tool), `{"type": "none"}` (don't use tools this turn).
- Claude can request **multiple tools in one turn** (parallel tool calls) — your response needs a `tool_result` for every `tool_use` block it sent, not just the first one.
- Tools fall into two buckets: **client tools** (yours — you write the code and execute it) and **server tools** (Anthropic's, like web search — they run automatically, no `tool_result` needed from you).

### 🟢 Lab 5.1 — Force a Specific Tool *(10 min)*
1. In the Workbench, with the `check_contract_status` tool still defined, set `tool_choice` to force that exact tool (via the Code view, since Form view may not expose this — add `"tool_choice": {"type": "tool", "name": "check_contract_status"}` to the request body).
2. Ask something unrelated: `What's the weather like today?`
3. Notice Claude is forced to call the tool anyway, awkwardly guessing a `vendor_name` — this is what over-forcing tool use looks like, and why `auto` is the sensible default for anything except narrow, single-purpose requests.

### 🔵 Lab 5.2 (Stretch) — Two Tools, Parallel Calls *(15 min)*
1. Extend `tool_loop.py` with a second tool and ask a question that plausibly needs both:
   ```python
   tools.append({
       "name": "get_todays_date",
       "description": "Returns today's date.",
       "input_schema": {"type": "object", "properties": {}},
   })

   messages = [{"role": "user", "content": (
       "What's today's date, and what's the renewal status of the "
       "Nimbus Cloud Services contract?"
   )}]
   response = client.messages.create(model="claude-sonnet-5", max_tokens=500, tools=tools, messages=messages)
   tool_uses = [b for b in response.content if b.type == "tool_use"]
   print(f"Claude requested {len(tool_uses)} tool call(s) in this turn: {[t.name for t in tool_uses]}")
   ```
2. Run it. If Claude requested both tools in the same turn, that's parallel tool use — your production code needs to loop over *every* `tool_use` block and return a matching `tool_result` for each one, not just handle the first.

---

## 6. Extended Thinking, Image & PDF Support

**Basic theory:**
- Extended thinking makes Claude show its reasoning in a separate `thinking` content block before its final answer.
- ⚠️ **Current models use adaptive thinking, not the older manual mode.** The old `{"type": "enabled", "budget_tokens": N}` syntax is deprecated and now **returns a 400 error** on current-generation models. Use `{"type": "adaptive"}` instead — Claude decides how much to think on its own.
- Vision: send an image as a content block (base64 or URL), supports JPEG/PNG/GIF/WebP, up to 20 images per request.
- PDFs use the same `document` content block type — Claude reads each page as an image, so PDF support inherits vision's strengths and limits.

### 🟢 Lab 6.1 — Turn On Adaptive Thinking *(10 min)*
1. In the Workbench (Code view, since this needs a body field the Form view may not expose), add:
   ```json
   "thinking": {"type": "adaptive"}
   ```
2. Ask: `A contract auto-renews unless cancelled 45 days before Oct 10, 2026. If today is August 1, 2026, is the cancellation deadline already in the past?`
3. Look for the separate thinking block above the final answer — check its date math by hand before trusting the final answer, same habit as every reasoning task today.

### 🔵 Lab 6.2 (Stretch) — Send an Image *(12 min)*
1. Save as `vision_demo.py` (use any real image file you have, or a screenshot of one of the sample contracts):
   ```python
   import base64
   from anthropic import Anthropic

   client = Anthropic()

   with open("contract_screenshot.png", "rb") as f:
       image_data = base64.b64encode(f.read()).decode("utf-8")

   response = client.messages.create(
       model="claude-sonnet-5",
       max_tokens=500,
       messages=[{
           "role": "user",
           "content": [
               {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
               {"type": "text", "text": "What vendor and end date does this contract show?"},
           ],
       }],
   )
   print(next(b.text for b in response.content if b.type == "text"))
   ```
2. Run it: `python vision_demo.py`. Compare Claude's answer against what the image actually says.

---

## 7. Prompt Caching, Citations & the Files API

**Basic theory:**
- **Prompt caching** lets Claude reuse a previously-processed prefix instead of reprocessing it — cheaper and faster for anything you send repeatedly (a long system prompt, a big document). Mark it with `cache_control`, either one top-level automatic marker or explicit markers on specific blocks.
- **Citations** ground Claude's answer in a source document and return the exact passage supporting each claim. They can't be combined with structured outputs (JSON schema) — the API returns a 400 error if you try both at once.
- The **Files API** lets you upload a file once and reference it by `file_id` in every future request, instead of re-sending the raw content every time.

### 🟢 Lab 7.1 — Citations on a Real Contract *(12 min)*
1. In the Workbench (Code view), send a document content block with citations enabled:
   ```json
   "messages": [{
     "role": "user",
     "content": [
       {
         "type": "document",
         "source": {"type": "text", "media_type": "text/plain", "data": "Nimbus Cloud Services. Contract NCS-2025-0142. Auto-renews for successive 12-month terms unless either party provides written notice of cancellation at least 30 days before the end date."},
         "citations": {"enabled": true}
       },
       {"type": "text", "text": "How much notice is required to cancel this contract?"}
     ]
   }]
   ```
2. Run it. Look for the citation reference pointing back to the exact sentence in the source document — not just an answer that sounds right, but one with a traceable receipt.

### 🔵 Lab 7.2 (Stretch) — Upload Once, Reuse the file_id *(15 min)*
1. Save as `files_demo.py`:
   ```python
   from anthropic import Anthropic

   client = Anthropic()

   file_obj = client.beta.files.upload(
       file=open("Contract_Nimbus_Cloud_Services.docx", "rb"),
   )
   print(f"Uploaded. file_id = {file_obj.id}")

   response = client.beta.messages.create(
       model="claude-sonnet-5",
       max_tokens=500,
       betas=["files-api-2025-04-14"],
       messages=[{
           "role": "user",
           "content": [
               {"type": "document", "source": {"type": "file", "file_id": file_obj.id}},
               {"type": "text", "text": "Summarize this contract in two sentences."},
           ],
       }],
   )
   print(next(b.text for b in response.content if b.type == "text"))
   ```
2. Run it: `python files_demo.py`. Note the `file_id` printed at the top — in a real application, you'd store that once and skip the upload step on every future request referencing the same file.

---

## 8. Code Execution & Context Management at Scale — Project

**Basic theory:**
- The **code execution tool** runs real Python/bash in a sandboxed container — Claude can analyze data, generate charts, and process uploaded files, not just describe what code *would* do.
- Long agentic conversations (lots of tool calls) eventually threaten the context window. **Compaction** (server-side, automatic summarization) is the primary fix for most cases. **Context editing** offers more surgical control — e.g., `clear_tool_uses` strips old tool results you no longer need, replacing them with a placeholder so Claude knows something was removed.
- Both are beta features requiring specific beta headers.

### 🔵 Project — Analyze the Course Dataset End to End *(30–40 min)*
Combine several of today's topics into one build: upload real data, have Claude analyze it with code execution, and manage context as the conversation grows.

1. Save the 5 course contracts' key facts as a CSV, `contracts.csv`:
   ```csv
   vendor,end_date,auto_renews,notice_days,annual_value
   Nimbus Cloud Services,2026-09-25,TRUE,30,63000
   BrightPath Security Solutions,2026-10-10,TRUE,45,24000
   Vertex Networking Group,2026-11-05,TRUE,60,19500
   Alderwood Office Supplies,2026-12-15,TRUE,60,4200
   Fixed-Term Consulting LLC,2026-09-20,FALSE,0,47000
   ```
2. Save as `project_code_exec.py`:
   ```python
   from anthropic import Anthropic

   client = Anthropic()

   file_obj = client.beta.files.upload(file=open("contracts.csv", "rb"))

   response = client.beta.messages.create(
       model="claude-sonnet-5",
       max_tokens=2048,
       betas=["files-api-2025-04-14", "code-execution-2025-05-22"],
       tools=[{"type": "code_execution_20250522", "name": "code_execution"}],
       messages=[{
           "role": "user",
           "content": [
               {"type": "container_upload", "file_id": file_obj.id},
               {"type": "text", "text": (
                   "Using this CSV, write and run Python to calculate total "
                   "annual_value for every contract where auto_renews is TRUE "
                   "and notice_days requires cancellation before Sept 1, 2026 "
                   "(assume today is August 1, 2026). Show your code and the result."
               )},
           ],
       }],
   )
   for block in response.content:
       if block.type == "text":
           print(block.text)
   ```
3. Run it. Compare the computed total against the `contract-review` Skill's answer from Module 3. *(Verified answer for this specific filter: Nimbus Cloud Services and BrightPath Security Solutions both have a notice deadline of Aug 26, 2026 — before the Sept 1 cutoff — for a combined total of $87,000. Everything else falls outside that window.)* This is the same underlying calculation, now done by real executed code instead of the model reasoning about numbers in its head.
4. **Context management extension:** if you continued this conversation with several more follow-up questions (each returning tool results), the message history would grow with every turn. Add `context_management` to a request to see the shape of automatic handling:
   ```python
   "context_management": {
       "edits": [{"type": "clear_tool_uses_20250919", "trigger": {"type": "input_tokens", "value": 3000}}]
   }
   ```
   You won't see this fire on one request, but this is the exact configuration a production agent uses to avoid ever hitting the context window limit during a long tool-calling session.

**Debrief:** which of today's 8 topics would you reach for first in a real project — and which one, honestly, are you still fuzzy on? Say it out loud; today's format assumed a lot of independent reading between labs, and that's worth naming if a topic didn't land.
