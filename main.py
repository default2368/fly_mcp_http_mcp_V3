#!/usr/bin/env python3
"""
MCP HTTP Server Standalone - Compatibile con Claude Desktop Remoto
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

try:
    # Try absolute import first (for when running as a module)
    from routes.mcp_routes import MCPRoutes
    from modules.mcp_methods import MCPMethods
except ImportError:
    # Fall back to relative import (for development)
    from .routes.mcp_routes import MCPRoutes
    from .modules.mcp_methods import MCPMethods

# Configurazione
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="MCP HTTP Server",
    description="Model Context Protocol Server over HTTP",
    version="1.0.0"
)

# CORS per client remoti
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import dei modelli Pydantic
from pydantic import BaseModel

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str | None = None
    method: str
    params: dict = {}

# Endpoint MCP Principale
@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    """Endpoint principale MCP over HTTP"""
    return await MCPRoutes.handle_mcp_request(request.dict())

# Endpoint aggiuntivi per monitoring
@app.get("/")
async def root():
    """Homepage con informazioni del server"""
    return {
        "service": "MCP HTTP Server",
        "version": "1.0.0",
        "status": "running",
        "mcp_endpoint": "/mcp",
        "health_endpoint": "/health",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check per deployment"""
    return {
        "status": "healthy",
        "service": "mcp-http-server",
        "protocol": "MCP over HTTP"
    }

@app.get("/tools")
async def list_tools_html():
    """Pagina HTML semplice con lista tools (opzionale)"""
    tools_info = [
        {"name": "get_server_info", "description": "Get server information and status"},
        {"name": "calculate_operation", "description": "Perform mathematical calculations"},
        {"name": "format_text", "description": "Format text in different styles"},
        {"name": "check_remote_health", "description": "Check health of remote URLs"}
    ]
    
    html_content = f"""
    <html>
        <head>
            <title>MCP HTTP Server Tools</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .tool {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .name {{ font-weight: bold; color: #333; }}
                .desc {{ color: #666; }}
            </style>
        </head>
        <body>
            <h1>MCP HTTP Server</h1>
            <p>Server running on {HOST}:{PORT}</p>
            <h2>Available Tools:</h2>
            {"".join([f'<div class="tool"><div class="name">{t["name"]}</div><div class="desc">{t["description"]}</div></div>' for t in tools_info])}
            <p><a href="/docs">API Documentation</a></p>
        </body>
    </html>
    """
    return HTMLResponse(html_content)

# Avvio del server
if __name__ == "__main__":
    print(f"🚀 Starting MCP HTTP Server on {HOST}:{PORT}")
    print(f"📚 API Docs: http://{HOST}:{PORT}/docs")
    print(f"🔧 MCP Endpoint: http://{HOST}:{PORT}/mcp")
    print(f"❤️  Health Check: http://{HOST}:{PORT}/health")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info" if not DEBUG else "debug"
    )