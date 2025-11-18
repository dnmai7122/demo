#!/usr/bin/env python3
"""
Main entry point for running the MCP server
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mcp_server.core.server import main

if __name__ == "__main__":
    print("🚀 Starting Sign Language DB MCP Server...")
    print("="*60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Server error: {str(e)}")
        sys.exit(1)

