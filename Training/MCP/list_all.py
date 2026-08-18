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