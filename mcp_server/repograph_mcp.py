from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import asyncio

app = Server("repograph")

@app.list_tools()
async def list_tools():
    pass


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    pass

async def main():
    async with stdio_server() as (read,write):
        await app.run(read, write, app.create_initialization_options())
        
asyncio.run(main())