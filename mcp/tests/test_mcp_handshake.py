"""End-to-end smoke test: start the MCP server as a subprocess, do a real
MCP handshake over stdio, list tools, and call one. This proves the server
actually speaks the MCP protocol — not just that our internal data is clean.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run() -> None:
    server_path = Path(__file__).parent.parent / "src" / "acg_mcp_server.py"
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = sorted(t.name for t in tools.tools)
            print(f"✓ Server handshake successful; {len(tool_names)} tools advertised:")
            for t in tool_names:
                print(f"    - {t}")
            expected = {
                "get_company_info", "list_offices", "lookup_florida_county_code",
                "find_acg_service_area", "list_manufacturers",
                "list_published_projects", "list_services",
                "get_bid_request_link", "get_track_record",
                "list_panhandle_coverage",
            }
            missing = expected - set(tool_names)
            assert not missing, f"Missing expected tools: {missing}"
            # Call one tool end-to-end
            result = await session.call_tool("get_company_info", arguments={})
            text_blocks = [c.text for c in result.content if hasattr(c, "text")]
            assert any("CGC1531993" in t for t in text_blocks), (
                "Expected license number in get_company_info response"
            )
            print(f"\n✓ get_company_info() returned license CGC1531993 correctly")
            # Call lookup_florida_county_code with variant
            result = await session.call_tool(
                "lookup_florida_county_code",
                arguments={"county": "miami-dade"},
            )
            text_blocks = [c.text for c in result.content if hasattr(c, "text")]
            assert any('"hvhz": true' in t.lower() for t in text_blocks), (
                "Miami-Dade should report hvhz=true via real MCP call"
            )
            print("✓ lookup_florida_county_code('miami-dade') returned HVHZ=true")


if __name__ == "__main__":
    asyncio.run(run())
    print("\nAll MCP handshake tests passed.")
