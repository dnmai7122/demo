#!/usr/bin/env python3
"""
Script to run MCP server for testing with MCP Inspector
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mcp_server.core.server import main

if __name__ == "__main__":
    print("🔍 Starting MCP Server for Inspector...", file=sys.stderr)
    print("="*60, file=sys.stderr)
    print("💡 Use this with MCP Inspector:", file=sys.stderr)
    print("   npx @modelcontextprotocol/inspector python run_mcp_inspector.py", file=sys.stderr)
    print("="*60, file=sys.stderr)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"\n\n❌ Server error: {str(e)}", file=sys.stderr)
        sys.exit(1)

