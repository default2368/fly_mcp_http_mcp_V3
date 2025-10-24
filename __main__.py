#!/usr/bin/env python3
"""
MCP HTTP Server - Entry Point
"""
from .main import app, HOST, PORT
import uvicorn

if __name__ == "__main__":
    print(f"🚀 Starting MCP HTTP Server on {HOST}:{PORT}")
    print(f"📚 API Docs: http://{HOST}:{PORT}/docs")
    uvicorn.run("claude_mcp_remote.main:app", 
                host=HOST, 
                port=PORT, 
                reload=True,
                log_level="info")
