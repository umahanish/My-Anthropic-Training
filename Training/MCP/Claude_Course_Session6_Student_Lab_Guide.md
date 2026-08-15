# Model Context Protocol (MCP) — Student Lab Guide
### Module 6: Standardizing How Claude Connects to Tools

New setup for this module — different packages, same contract scenario.

```bash
pip install fastmcp mcp
```

**Two different "FastMCP"s exist — worth knowing before you start:** `fastmcp` (what we install above) is a popular, actively developed standalone package. The base `mcp` SDK also ships its own smaller `mcp.server.fastmcp` module with a similar name. This module uses the standalone `fastmcp` package throughout, since it's what most real-world MCP servers are actually built with today.

**Legend:** 🟢 Core (Inspector UI, minimal/no code) · 🔵 Stretch (real Python scripts)

**Running scenario, once more extended:** Module 5 built a system that *finds* the right contract. This module wraps that same contract data as an MCP **server** — a standard, reusable interface that Claude Desktop, Claude Code, or any other MCP-compatible application could plug into, instead of custom-wiring your contract lookup into every single app separately.

---

## 1. MCP Architecture: Servers, Clients & Transports
**Format: Reading — no lab, ~10 min**

**The core problem MCP solves:** without a standard, connecting *N* AI applications to *M* external tools means building *N × M* custom integrations. MCP turns that into *N + M* — every tool builds one MCP server, every application builds one MCP client, and they all speak the same protocol to each other.

**Three architectural roles, not two:**
- **Host** — the AI application the user actually interacts with (Claude Desktop, Claude Code, your own app).
- **Client** — lives inside the host, maintains a strict 1:1 connection to exactly one server.
- **Server** — a separate, focused program that exposes **tools** (actions), **resources** (data), and **prompts** (reusable templates) via MCP.

A host can run many clients at once — one per connected server — which is exactly what you saw in Module 3's Cowork plugins, each of which is very likely an MCP server under the hood.

**Everything rides on JSON-RPC 2.0.** Every message — requests, responses, notifications — follows that base spec. MCP adds the vocabulary on top (what a "tool call" message looks like, what a "resource read" looks like), but the envelope is always JSON-RPC.

**Capability negotiation:** client and server declare what they each support right when the connection opens — a client might not support sampling, a server might not offer resources — and both sides are expected to respect what was actually negotiated for the rest of the session.

**Transports — how the JSON-RPC messages actually travel:**
- **stdio** — standard input/output. Used for local servers running as a subprocess on the same machine. Simple, fast, no network involved.
- **Streamable HTTP** — the current standard transport for remote servers, replacing the older HTTP+SSE approach. One HTTP endpoint handles both directions.
- **SSE (Server-Sent Events)** — the older remote transport. Still supported for backward compatibility, but Streamable HTTP is what new remote servers should use.

---

## 2. Defining Tools with MCP & the Server Inspector

**Basic theory:**
- An MCP tool looks almost exactly like the Claude API tools from Module 4 — a name, a description, and a schema — except here, the schema is generated automatically from your Python function's type hints and docstring. You don't hand-write JSON Schema.
- The **MCP Inspector** is the standard way to test a server without wiring up a full client or host application — think of it as Postman, but for MCP.

### 🟢 Lab 2.1 — Build a Server, Inspect It Live *(15 min)*
1. Save as `contract_server.py`:
   ```python
   from fastmcp import FastMCP

   mcp = FastMCP("Contract Server")

   CONTRACTS = {
       "nimbus cloud services": {
           "end_date": "2026-09-25", "auto_renews": True,
           "notice_days": 30, "annual_value": 63000,
       },
       "brightpath security solutions": {
           "end_date": "2026-10-10", "auto_renews": True,
           "notice_days": 45, "annual_value": 24000,
       },
   }

   @mcp.tool()
   def check_contract_status(vendor_name: str) -> dict:
       """Look up the renewal status of a vendor contract by vendor name."""
       return CONTRACTS.get(vendor_name.lower(), {"error": "No record found for that vendor."})

   if __name__ == "__main__":
       mcp.run()
   ```
2. In a terminal, run the Inspector pointed at your server:
   ```bash
   npx @modelcontextprotocol/inspector python contract_server.py
   ```
3. It opens a browser UI (usually `http://localhost:6274`) with a proxy running on port 6277, and prints a session token — open the printed URL, don't navigate there manually without it.
4. In the Inspector, find `check_contract_status` under **Tools**, fill in `vendor_name` with `Nimbus Cloud Services`, and run it. Confirm the returned JSON matches what's in your `CONTRACTS` dict.

### 🔵 Lab 2.2 (Stretch) — Same Tool, Programmatic Test *(10 min)*
1. Save as `test_tool.py`:
   ```python
   import asyncio
   from fastmcp import Client
   from contract_server import mcp

   async def main():
       async with Client(mcp) as client:
           tools = await client.list_tools()
           print("Tools found:", [t.name for t in tools])
           result = await client.call_tool("check_contract_status", {"vendor_name": "Nimbus Cloud Services"})
           print("Result:", result.data)

   asyncio.run(main())
   ```
2. Run it: `python test_tool.py`. `Client(mcp)` connecting directly to the server object, no subprocess or network involved, is the fastest way to test a server in code — this is what you'd actually use in a test suite, not the Inspector.

---

## 3. Implementing MCP Clients & Resources

**Basic theory:**
- A **resource** exposes data (not an action) — the MCP equivalent of a GET endpoint. Resources are identified by URIs you define, like `contract://nimbus-cloud-services`.
- A client is the piece of code that actually connects to a server and calls its tools/resources/prompts — everything in Lab 2.2 was already a minimal client.
- **⚠️ URIs can't contain raw spaces or other unsafe characters** — this bit me while building this exact lab, so it's worth knowing up front rather than discovering it the hard way mid-class.

### 🟢 Lab 3.1 — Add a Resource, Break It on Purpose *(12 min)*
1. Add this to `contract_server.py`, above the `if __name__ == "__main__":` line:
   ```python
   @mcp.resource("contract://{vendor_name}")
   def get_contract_resource(vendor_name: str) -> dict:
       """Expose a contract's raw data as a resource."""
       return CONTRACTS.get(vendor_name.lower(), {"error": "No record found for that vendor."})
   ```
2. Re-run the Inspector (`npx @modelcontextprotocol/inspector python contract_server.py`), find **Resources**, and try reading `contract://Nimbus Cloud Services` — the raw name, with a space in it.
3. Watch it fail with a URL-parsing error. That's not a bug in your server — URIs are not allowed to contain a literal space.

### 🔵 Lab 3.2 (Stretch) — Fix It Properly in Code *(10 min)*
1. Save as `test_resource.py`:
   ```python
   import asyncio
   from urllib.parse import quote
   from fastmcp import Client
   from contract_server import mcp

   async def main():
       async with Client(mcp) as client:
           encoded_name = quote("Nimbus Cloud Services")  # -> "Nimbus%20Cloud%20Services"
           result = await client.read_resource(f"contract://{encoded_name}")
           print(result[0].text)

   asyncio.run(main())
   ```
2. Run it: `python test_resource.py`. This should now succeed — `urllib.parse.quote` is the fix, not avoiding vendor names with spaces in your real data.

---

## 4. Prompts in MCP & JSON Message Types

**Basic theory:**
- An MCP **prompt** is a reusable template a server offers — the server defines the shape, the client/host fills in arguments and gets back a ready-to-use message. It's the MCP equivalent of a saved prompt you'd reuse across conversations.
- Underneath every tool call, resource read, and prompt request is a JSON-RPC message. Knowing the shape helps you actually read Inspector's raw traffic when something goes wrong.

### 🟢 Lab 4.1 — Add a Prompt, Watch It in the Inspector *(10 min)*
1. Add this to `contract_server.py`:
   ```python
   @mcp.prompt()
   def renewal_review_prompt(vendor_name: str) -> str:
       """Create a prompt template for reviewing a contract's renewal risk."""
       return f"Review the renewal terms for {vendor_name} and flag any urgent action needed."
   ```
2. Re-run the Inspector. Find **Prompts**, select `renewal_review_prompt`, fill in `vendor_name`, and generate it.
3. Look for a way to view the raw request/response in the Inspector (often a details or JSON toggle). You're looking for something shaped like this underneath:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "prompts/get",
     "params": {
       "name": "renewal_review_prompt",
       "arguments": {"vendor_name": "Nimbus Cloud Services"}
     }
   }
   ```

### 🔵 Lab 4.2 (Stretch) — List Everything Programmatically *(10 min)*
1. Save as `list_all.py`:
   ```python
   import asyncio
   from fastmcp import Client
   from contract_server import mcp

   async def main():
       async with Client(mcp) as client:
           print("Tools:", [t.name for t in await client.list_tools()])
           print("Prompts:", [p.name for p in await client.list_prompts()])
           # Note: resources with URI templates (like contract://{vendor_name})
           # are "resource templates," listed separately from static resources.
           templates = await client.list_resource_templates()
           print("Resource templates:", [t.uriTemplate for t in templates])

   asyncio.run(main())
   ```
2. Run it: `python list_all.py`. This is the same `list_tools`/`list_prompts`/`list_resource_templates` machinery a real host application uses to discover what your server offers before showing it to a user or Claude.

---

## 5. Streamable HTTP Transport & State Management

**Basic theory:**
- Everything so far ran over **stdio** — your server as a local subprocess. Real deployed servers usually run over HTTP so multiple clients, possibly on different machines, can reach the same server.
- Streamable HTTP is stateful by default: the server assigns a session ID on connection (an `Mcp-Session-Id` header) and the SDK tracks it automatically — you don't manage this by hand in normal use, but it's worth knowing it exists when debugging.

### 🟢 Lab 5.1 — Run Your Server Over HTTP Instead *(12 min)*
1. Change the bottom of `contract_server.py`:
   ```python
   if __name__ == "__main__":
       mcp.run(transport="streamable-http")
   ```
2. Run it: `python contract_server.py`. It should now start an HTTP server (commonly on port 8000) instead of waiting on stdio.
3. Open the Inspector fresh (`npx @modelcontextprotocol/inspector`, with no server command this time), select **Streamable HTTP** as the transport in the UI, and enter your server's URL (typically `http://localhost:8000/mcp`). Connect, and confirm your tool/resource/prompt all still show up — same server code, different transport, same capabilities.

### 🔵 Lab 5.2 (Stretch) — Connect a Client Over HTTP *(10 min)*
1. Save as `http_client.py`:
   ```python
   import asyncio
   from fastmcp import Client

   async def main():
       # A URL string instead of a server object -- this is the only
       # change needed to talk to a remote server instead of an in-memory one.
       async with Client("http://localhost:8000/mcp") as client:
           result = await client.call_tool("check_contract_status", {"vendor_name": "Nimbus Cloud Services"})
           print(result.data)

   asyncio.run(main())
   ```
2. With `contract_server.py` still running from Lab 5.1 in another terminal, run: `python http_client.py`.
3. Notice the client code is nearly identical to Lab 2.2's in-memory version — swapping a server object for a URL string is the entire difference between "testing locally" and "talking to a real deployed server."

---

## 6. MCP Advanced: Sampling, Logging & Notifications — Project

**Basic theory:**
- **Logging** — a server sends log messages to the client mid-task (`ctx.info()`, `ctx.warning()`) so a human watching can see progress. Stable, uncontroversial, works the same across MCP versions.
- **Sampling** — a server asks the *client's* LLM to generate text on its behalf (`ctx.sample()`), rather than the server needing its own API key and model access. This lets a lightweight server borrow intelligence from whatever host it's plugged into.
- **Notifications** — fire-and-forget messages, like "my resource list just changed" — the server doesn't wait for a reply.

**⚠️ Read this before building the sampling part.** MCP's July 2026 protocol revision **removed server-initiated sampling from the protocol itself** (a change called SEP-2577), because the modern protocol moved toward being fully stateless, and a stateless server has no persistent channel to push a request into. FastMCP's own 4.x line drops `ctx.sample()` as a direct consequence. **The version this guide verified against — `fastmcp` 3.4.7, what a plain `pip install fastmcp` gives you right now — still has it.** If `ctx.sample()` raises an `AttributeError` for you, that's not a mistake on your part — it means you're on FastMCP 4+, where this was intentionally removed, and the fallback is calling an LLM provider directly from inside the tool (exactly what Module 4 already taught you to do).

### 🔵 Project — A Server That Logs, Samples, and Notifies *(30 min)*
1. Add this to `contract_server.py`:
   ```python
   from fastmcp import Context

   @mcp.tool()
   async def summarize_contract_risk(vendor_name: str, ctx: Context) -> str:
       """Summarize a contract's renewal risk using the client's own LLM."""
       await ctx.info(f"Looking up {vendor_name}...")
       contract = CONTRACTS.get(vendor_name.lower())
       if not contract:
           await ctx.warning(f"No record found for {vendor_name}")
           return "No record found for that vendor."

       await ctx.info("Asking the client's LLM to summarize risk...")
       result = await ctx.sample(
           messages=(
               f"Contract for {vendor_name}: ends {contract['end_date']}, "
               f"auto-renews: {contract['auto_renews']}, "
               f"notice required: {contract['notice_days']} days. "
               "In one sentence, state the renewal risk."
           ),
           system_prompt="You are a concise contract risk analyst.",
       )
       return result.text
   ```
2. Test it via the Inspector (stdio, like Lab 2.1) — call `summarize_contract_risk` with `vendor_name: Nimbus Cloud Services`. Watch for the log messages appearing separately from the final result — that's `ctx.info()` reaching the Inspector mid-call, before the tool has even finished.
3. If sampling fails because the Inspector doesn't have a configured LLM to sample from, that's expected in a bare test harness — the concept to take away is the *shape* of the exchange (server asks, waits, receives, continues), which is identical whether the sampling handler is the Inspector, Claude Desktop, or a client you write yourself with a real `sampling_callback`.

**Debrief:** this module was built on a protocol that changed a fundamental capability (sampling) three weeks before this class existed. What's your plan for a production MCP server you actually ship — pin your `fastmcp` version deliberately, or build without relying on sampling at all and call an LLM directly like Module 4 taught? There's a real trade-off either way, and "the protocol might change under me" is a genuinely different risk profile than anything else in this course so far.
