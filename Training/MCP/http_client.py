import asyncio
from fastmcp import Client

async def main():
    # A URL string instead of a server object -- this is the only
    # change needed to talk to a remote server instead of an in-memory one.
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.call_tool("check_contract_status", {"vendor_name": "Nimbus Cloud Services"})
        print(result.data)

asyncio.run(main())