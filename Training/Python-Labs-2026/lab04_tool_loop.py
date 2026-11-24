"""Lab 4.2: complete a tool-use loop in code, with a step cap.

Run: python lab04_tool_loop.py --mock   (offline)   or   python lab04_tool_loop.py   (live)
"""
from common import SONNET, get_client, text_of

CONTRACTS = {
    "nimbus cloud services": {"end_date": "2026-09-25", "auto_renews": True, "notice_days": 30},
    "vertex networking group": {"end_date": "2026-11-05", "auto_renews": True, "notice_days": 60},
}
TODAY = "2026-08-01"  # fixed for the course scenario

TOOLS = [
    {
        "name": "check_contract_status",
        "description": "Look up a vendor contract by vendor name. Returns end date, notice days and auto-renewal.",
        "input_schema": {
            "type": "object",
            "properties": {"vendor_name": {"type": "string"}},
            "required": ["vendor_name"],
        },
    },
    {
        "name": "get_today",
        "description": "Returns today's date for the course scenario.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


def run_tool(name: str, args: dict) -> str:
    if name == "check_contract_status":
        record = CONTRACTS.get(args.get("vendor_name", "").lower())
        return str(record) if record else "No record found for that vendor."
    if name == "get_today":
        return TODAY
    return f"Unknown tool: {name}"


def ask(client, question: str, max_steps: int = 5) -> str:
    messages = [{"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        resp = client.messages.create(
            model=SONNET,
            max_tokens=600,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return text_of(resp)
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                output = run_tool(block.name, block.input)
                print(f"  step {step}: {block.name}({block.input}) -> {output}")
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})
        messages.append({"role": "user", "content": results})
    return "Stopped: step limit reached."


def mock_responder(kw: dict):
    last = kw["messages"][-1]["content"]
    if isinstance(last, list) and last and last[0].get("type") == "tool_result":
        return "The deadline is 2026-08-26 (2026-09-25 minus 30 days), so it has not passed yet."
    names = {m["content"][0]["name"] for m in kw["messages"] if m["role"] == "assistant"} if len(kw["messages"]) > 1 else set()
    tool = "get_today" if "check_contract_status" in names else "check_contract_status"
    args = {} if tool == "get_today" else {"vendor_name": "Nimbus Cloud Services"}
    return [{"type": "tool_use", "id": f"toolu_{tool}", "name": tool, "input": args}]


if __name__ == "__main__":
    client = get_client(mock_responder)
    print(ask(client, "Is the Nimbus contract's cancellation deadline already past? Show the date."))
