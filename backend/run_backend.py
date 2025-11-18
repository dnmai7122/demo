#!/usr/bin/env python3
"""
Script to run FastAPI backend server
"""

import uvicorn
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    print("🚀 Starting FastAPI Backend Server...")
    print("="*60)
    print("📍 Server running on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📋 Alternative docs: http://localhost:8000/redoc")
    print("="*60)
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

