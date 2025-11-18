"""
Main MCP Server implementation
"""

import asyncio
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio

from .config import config


class MCPServer:
    """Main MCP Server class"""
    
    def __init__(self):
        """Initialize MCP server with configuration"""
        # Validate configuration
        config.validate()
        
        # Initialize server
        self.server = Server(config.SERVER_NAME)
        
        # Initialize tools (empty for now - product tools removed)
        self.tools = {}
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            tools_list = []
            for tool_name, tool_instance in self.tools.items():
                tools_list.append(tool_instance.get_definition())
            return tools_list
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls"""
            try:
                if name not in self.tools:
                    return [TextContent(
                        type="text",
                        text=f"❌ Lỗi: Tool '{name}' không tồn tại"
                    )]
                
                tool = self.tools[name]
                result = await tool.execute(arguments)
                return result
            
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Lỗi khi thực thi tool '{name}': {str(e)}"
                )]
    
    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


# Main entry point
async def main():
    """Main entry point for MCP server"""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

