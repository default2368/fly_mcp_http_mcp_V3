#!/usr/bin/env python3
"""
MCP HTTP Server - Entry Point
"""
import os
import sys

# Add the current directory to the path to ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, HOST, PORT
import uvicorn

if __name__ == "__main__":
    print(f"🚀 Starting MCP HTTP Server on {HOST}:{PORT}")
    print(f"📚 API Docs: http://{HOST}:{PORT}/docs")
    
    # Use reload only in development
    reload = os.environ.get("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=reload,
        log_level="info"
    )
