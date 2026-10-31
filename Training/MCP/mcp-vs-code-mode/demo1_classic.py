# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp==2.3.0", "anthropic"]
# ///
"""DEMO 1 - Classic MCP: Claude sees every MCP tool and calls them one at a time.
Every tool result goes back through the model before the next step.

    ANTHROPIC_API_KEY=... uv run demo1_classic.py
"""

import asyncio
import json
import sys
import time

import anthropic

from mcp import Client, StdioServerParameters

MODEL = "claude-sonnet-5-5"
TASK = sys.argv[1] if len(sys.argv) > 1 else (
    "Check the weather in all our office cities, find the warmest city that is not rainy or stormy, "
    "and book me a flight there on 2026-11-20."
)


async def main() -> None:
    t0 = time.time()
    stats = {"llm_calls": 0, "mcp_tool_calls": 0, "in_tokens": 0, "out_tokens": 0}

    print("\n=== DEMO 1: Classic MCP ===")
    print("STEP 1: connect to the MCP server (stdio)")
    server = StdioServerParameters(command="uv", args=["run", "-q", "travel_server.py"])
    async with Client(server) as mcp:
        print("STEP 2: list tools and hand ALL of them to Claude")
        listed = await mcp.list_tools()
        tools = [{"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in listed.tools]
        print(f"  tools: {[t['name'] for t in tools]}")

        print(f"STEP 3: give Claude the task\n  user: {TASK}")
        claude = anthropic.AsyncAnthropic()
        messages = [{"role": "user", "content": TASK}]
        while True:
            resp = await claude.messages.create(model=MODEL, max_tokens=2048, tools=tools, messages=messages)
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
                stats["mcp_tool_calls"] += 1
                out = await mcp.call_tool(block.name, block.input)
                text = json.dumps(out.structured_content, separators=(",", ":")) if out.structured_content else "".join(
                    c.text for c in out.content if c.type == "text")
                flat = " ".join(text.split())
                shown = flat if len(flat) < 110 else f"{flat[:80]}... ({len(text)} chars sent to Claude)"
                print(f"  [LLM turn {stats['llm_calls']}] Claude -> MCP {block.name}({block.input}) => {shown}")
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": text})
            messages.append({"role": "user", "content": results})

        print("STEP 4: Claude's final answer")
        print("  " + "".join(b.text for b in resp.content if b.type == "text").replace("\n", "\n  "))
    print(f"\nSTATS  LLM calls={stats['llm_calls']}  MCP tool calls={stats['mcp_tool_calls']}  "
          f"input tokens={stats['in_tokens']}  output tokens={stats['out_tokens']}  time={time.time() - t0:.1f}s")


asyncio.run(main())
