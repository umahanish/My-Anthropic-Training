import os
from pathlib import Path

from dotenv import dotenv_values
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY") or dotenv_values(
    Path(__file__).resolve().parents[2] / ".env"
).get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is missing. Set it in the environment or the repository .env file."
    )

client = Anthropic(api_key=api_key)

CONTRACTS = {
    "nimbus cloud services": {"end_date": "2026-09-25", "auto_renews": True, "notice_days": 30},
}

def check_contract_status(vendor_name: str) -> str:
    c = CONTRACTS.get(vendor_name.lower())
    return str(c) if c else "Not found."

def get_todays_date() -> str:
    return "2026-08-01"  # fixed for this course's scenario

tools = [
    {"name": "check_contract_status", "description": "Look up a contract by vendor name.",
     "input_schema": {"type": "object", "properties": {"vendor_name": {"type": "string"}}, "required": ["vendor_name"]}},
    {"name": "get_todays_date", "description": "Returns today's date.",
     "input_schema": {"type": "object", "properties": {}}},
]

messages = [{"role": "user", "content": "Is the Nimbus contract's cancellation deadline already in the past?"}]

for _ in range(4):  # loop until Claude stops requesting tools
    response = client.messages.create(model="claude-sonnet-5", max_tokens=500, tools=tools, messages=messages)
    messages.append({"role": "assistant", "content": response.content})
    if response.stop_reason != "tool_use":
        print(next(b.text for b in response.content if b.type == "text"))
        break
    results = []
    for block in response.content:
        if block.type == "tool_use":
            fn = {"check_contract_status": check_contract_status, "get_todays_date": get_todays_date}[block.name]
            result = fn(**block.input)
            print(f"  [environment inspected: {block.name}({block.input}) -> {result}]")
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
    messages.append({"role": "user", "content": results})