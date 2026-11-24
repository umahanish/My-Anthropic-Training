"""Lab 6: a small MCP server exposing contract data.

Run the Inspector:  npx @modelcontextprotocol/inspector python lab06_contract_server.py
Test in code:       python lab06_contract_server.py --test
"""
import asyncio
import sys
from urllib.parse import quote

from fastmcp import Client, FastMCP

mcp = FastMCP("Contract Server")

CONTRACTS = {
    "nimbus cloud services": {"end_date": "2026-09-25", "auto_renews": True, "notice_days": 30},
    "brightpath security solutions": {"end_date": "2026-10-10", "auto_renews": True, "notice_days": 45},
}


@mcp.tool()
def check_contract_status(vendor_name: str) -> dict:
    """Look up the renewal status of a vendor contract by vendor name."""
    return CONTRACTS.get(vendor_name.strip().lower(), {"error": "No record found for that vendor."})


@mcp.resource("contract://{vendor_name}")
def contract_resource(vendor_name: str) -> dict:
    """A contract record as a resource. Clients must percent-encode the name."""
    return CONTRACTS.get(vendor_name.strip().lower(), {"error": "No record found for that vendor."})


async def self_test() -> None:
    async with Client(mcp) as client:
        tools = [t.name for t in await client.list_tools()]
        print("Tools:", tools)
        result = await client.call_tool("check_contract_status", {"vendor_name": "Nimbus Cloud Services"})
        print("Tool result:", result.data)
        resource = await client.read_resource(f"contract://{quote('Nimbus Cloud Services')}")
        print("Resource:", resource[0].text)


if __name__ == "__main__":
    if "--test" in sys.argv:
        asyncio.run(self_test())
    else:
        mcp.run()
