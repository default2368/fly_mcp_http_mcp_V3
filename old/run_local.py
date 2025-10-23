#!/usr/bin/env python3
"""
Local development server for FastMPC MCP Server
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config

app = FastAPI(title="FastMPC MCP Server")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "FastMPC MCP Server",
        "version": "1.0.0"
    }

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            "get_server_info",
            "calculate_operation",
            "format_text",
            "get_system_status"
        ]
    }

if __name__ == "__main__":
    port = 8000  # Set the port to 8000
    print("🚀 Starting FastMPC MCP Server...")
    print(f"🌐 Server running on http://{Config.HOST}:{port}")
    print(f"🔧 Debug mode: {'ON' if Config.DEBUG else 'OFF'}")
    print(f"⚡ FastMPC Enabled: {Config.FASTMPC_ENABLED}")
    if Config.FASTMPC_ENABLED:
        print(f"🔌 FastMPC Endpoint: {Config.FASTMPC_ENDPOINT}")
    
    uvicorn.run(
        "run_local:app",
        host=Config.HOST,
        port=port,  # Use the port variable set above
        reload=Config.DEBUG,
        log_level=Config.LOG_LEVEL.lower()
    )
