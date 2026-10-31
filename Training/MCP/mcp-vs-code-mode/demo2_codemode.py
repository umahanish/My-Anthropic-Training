"""DEMO 2 (Python) - Code Mode (UTCP): Claude gets ONE tool, writes Python, and a
RestrictedPython sandbox calls the same MCP server's tools directly.

Runs in its own venv (utcp-mcp needs mcp<2, the classic demo uses mcp 2.x):
    source .venv-codemode/bin/activate
    ANTHROPIC_API_KEY=... python demo2_codemode.py
"""

import asyncio
import json
import logging
import operator
import sys
import time
import warnings

import anthropic
import utcp_mcp  # noqa: F401  (registers the 'mcp' call template)
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.Guards import full_write_guard, guarded_iter_unpack_sequence, guarded_unpack_sequence
from utcp_code_mode import CodeModeUtcpClient
from utcp_mcp import McpCallTemplate

logging.disable(logging.WARNING)
warnings.filterwarnings("ignore", category=SyntaxWarning)

MODEL = "claude-sonnet-5-5"
TASK = sys.argv[1] if len(sys.argv) > 1 else (
    "Check the weather in all our office cities, find the warmest city that is not rainy or stormy, "
    "and book me a flight there on 2026-11-20."
)
stats = {"llm_calls": 0, "mcp_tool_calls": 0, "in_tokens": 0, "out_tokens": 0}

INPLACE = {"+=": operator.iadd, "-=": operator.isub, "*=": operator.imul, "/=": operator.itruediv}


class CodeMode(CodeModeUtcpClient):
    """code-mode 1.1.0 compatibility fixes (the Python package lags the TypeScript one)."""

    async def close(self):
        # utcp 1.2 made close() abstract; code-mode 1.1.0 never implemented it.
        await self._base_client.close()

    async def call_tool(self, name, args):
        # Sandboxed code calls tools from a worker thread with its own event loop, but the
        # MCP stdio session lives on the main loop -> hop back to it, or the call hangs forever.
        stats["mcp_tool_calls"] += 1
        print(f"  [sandbox -> MCP] {name}({json.dumps(args)})")
        if asyncio.get_running_loop() is self.home:
            return await self._base_client.call_tool(name, args)
        fut = asyncio.run_coroutine_threadsafe(self._base_client.call_tool(name, args), self.home)
        return await asyncio.wrap_future(fut)

    async def _create_execution_context(self, tools, logs=None):
        # RestrictedPython's standard guards are missing, so loops and d['key'] fail without them.
        ctx = await super()._create_execution_context(tools, logs)
        ctx.update(
            _getiter_=default_guarded_getiter, _getitem_=default_guarded_getitem, _write_=full_write_guard,
            _iter_unpack_sequence_=guarded_iter_unpack_sequence, _unpack_sequence_=guarded_unpack_sequence,
            _inplacevar_=lambda op, x, y: INPLACE[op](x, y),
        )
        # ...and so are some everyday builtins.
        ctx["__builtins__"].update(any=any, all=all, list=list, dict=dict, set=set)
        return ctx


async def main() -> None:
    t0 = time.time()
    print("\n=== DEMO 2 (Python): Code Mode ===")
    print("STEP 1: register the MCP server with Code Mode")
    codemode = await CodeMode.create()
    codemode.home = asyncio.get_running_loop()
    await codemode.register_manual(McpCallTemplate(
        name="travel", call_template_type="mcp",
        config={"mcpServers": {"travel": {"transport": "stdio", "command": "uv", "args": ["run", "-q", "travel_server.py"]}}},
    ))

    print("STEP 2: turn MCP tools into Python interfaces for the prompt")
    interfaces = await codemode.get_all_tools_python_interfaces()
    system = (
        f"{CodeModeUtcpClient.AGENT_PROMPT_TEMPLATE}\n\nAvailable tool interfaces:\n{interfaces}\n\n"
        "Do the whole task in ONE call_tool_chain when you can: fetch, filter, decide and act inside the code, "
        "and return only a small summary. Call tools with keyword args, e.g. travel.get_weather(city='Tokyo')."
    )

    # The ONLY tool Claude sees.
    tools = [{
        "name": "call_tool_chain",
        "description": "Execute Python code with access to all registered tools. Returns {result, logs}.",
        "input_schema": {"type": "object", "properties": {"code": {"type": "string", "description": "Python function body; use return for the result."}}, "required": ["code"]},
    }]

    print(f"STEP 3: give Claude the task + 1 tool (call_tool_chain)\n  user: {TASK}")
    claude = anthropic.AsyncAnthropic()
    messages = [{"role": "user", "content": TASK}]
    while True:
        resp = await claude.messages.create(model=MODEL, max_tokens=2048, system=system, tools=tools, messages=messages)
        stats["llm_calls"] += 1
        stats["in_tokens"] += resp.usage.input_tokens
        stats["out_tokens"] += resp.usage.output_tokens
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            break
        results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            print("STEP 4: Claude wrote this code:\n" + "\n".join(f"    | {line}" for line in block.input["code"].splitlines()))
            out = await codemode.call_tool_chain(block.input["code"])
            print(f"  sandbox result: {json.dumps(out['result'], default=str)}")
            if out["result"] is None:
                print(f"  sandbox logs: {' | '.join(out['logs'])[:300]}")
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(out, default=str)})
        messages.append({"role": "user", "content": results})

    print("STEP 5: Claude's final answer")
    print("  " + "".join(b.text for b in resp.content if b.type == "text").replace("\n", "\n  "))
    print(f"\nSTATS  LLM calls={stats['llm_calls']}  MCP tool calls={stats['mcp_tool_calls']}  "
          f"input tokens={stats['in_tokens']}  output tokens={stats['out_tokens']}  time={time.time() - t0:.1f}s")
    await codemode.close()


asyncio.run(main())
