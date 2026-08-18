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