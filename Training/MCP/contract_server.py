from fastmcp import Context, FastMCP

mcp = FastMCP("Contract Server")

CONTRACTS = {
    "nimbus cloud services": {
        "end_date": "2026-09-25",
        "auto_renews": True,
        "notice_days": 30,
        "annual_value": 63000,
    },
    "brightpath security solutions": {
        "end_date": "2026-10-10",
        "auto_renews": True,
        "notice_days": 45,
        "annual_value": 24000,
    },
}

@mcp.tool()
def check_contract_status(vendor_name: str) -> dict:
    """Look up the renewal status of a vendor contract by vendor name."""
    return CONTRACTS.get(vendor_name.lower(), {"error": "No record found for that vendor."})


@mcp.resource("contract://{vendor_name}")
def get_contract_resource(vendor_name: str) -> dict:
    """Expose a contract's raw data as a resource."""
    return CONTRACTS.get(vendor_name.lower(), {"error": "No record found for that vendor."})


@mcp.prompt()
def renewal_review_prompt(vendor_name: str) -> str:
    """Create a prompt template for reviewing a contract's renewal risk."""
    return f"Review the renewal terms for {vendor_name} and flag any urgent action needed."


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


if __name__ == "__main__":
    mcp.run()