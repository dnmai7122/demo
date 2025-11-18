"""
Base class for MCP tools
"""

from abc import ABC, abstractmethod
from typing import Any, Sequence
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource


class BaseTool(ABC):
    """Abstract base class for all MCP tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_definition(self) -> Tool:
        """
        Return the tool definition for MCP
        
        Returns:
            Tool object with name, description, and input schema
        """
        pass
    
    @abstractmethod
    async def execute(self, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """
        Execute the tool with given arguments
        
        Args:
            arguments: Tool arguments dictionary
            
        Returns:
            Sequence of content objects (typically TextContent)
        """
        pass
    
    def _create_text_response(self, text: str) -> Sequence[TextContent]:
        """
        Helper method to create text response
        
        Args:
            text: Response text
            
        Returns:
            List with single TextContent object
        """
        return [TextContent(type="text", text=text)]
    
    def _create_error_response(self, error_message: str) -> Sequence[TextContent]:
        """
        Helper method to create error response
        
        Args:
            error_message: Error message
            
        Returns:
            List with single TextContent object containing error
        """
        return [TextContent(type="text", text=f"❌ Lỗi: {error_message}")]

