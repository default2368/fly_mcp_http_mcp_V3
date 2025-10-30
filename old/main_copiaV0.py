#!/usr/bin/env python3
"""
MCP HTTP Server Standalone - Compatibile con Claude Desktop Remoto
"""
import json
import os
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from pydantic import BaseModel

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
    allow_origins=["*"],  # In produzione, specifica gli origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Strutture dati
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str | None = None
    method: str
    params: Dict[str, Any] = {}

class ToolCallArguments(BaseModel):
    operation: str | None = None
    text: str | None = None
    style: str | None = None
    url: str | None = None

# Logica Tools
def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Esegue il tool specificato con gli argomenti forniti"""
    
    if tool_name == "get_server_info":
        return json.dumps({
            "server_name": "MCP HTTP Server",
            "version": "1.0.0",
            "status": "running",
            "protocol": "HTTP",
            "endpoint": f"http://{HOST}:{PORT}/mcp",
            "message": "Hello from Remote MCP Server!"
        }, indent=2)
    
    elif tool_name == "calculate_operation":
        operation = arguments.get("operation", "")
        if not operation:
            return "Error: Operation parameter is required"
        
        try:
            # Calcolo sicuro - sostituisce eval()
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in operation.replace(' ', '')):
                result = eval(operation)  # ⚠️ In produzione usa una libreria sicura
                return f"Calculation: {operation} = {result}"
            else:
                return "Error: Operation contains unsafe characters"
        except Exception as e:
            return f"Error calculating operation: {e}"
    
    elif tool_name == "format_text":
        text = arguments.get("text", "")
        style = arguments.get("style", "uppercase")
        
        if not text:
            return "Error: Text parameter is required"
        
        styles = {
            "uppercase": text.upper(),
            "lowercase": text.lower(),
            "title": text.title(),
            "capitalize": text.capitalize()
        }
        
        if style in styles:
            return f"Formatted text ({style}): {styles[style]}"
        else:
            return f"Error: Unknown style '{style}'. Available: {list(styles.keys())}"
    
    elif tool_name == "check_remote_health":
        url = arguments.get("url", "https://httpbin.org/status/200")
        
        try:
            response = requests.get(url, timeout=10)
            status = "healthy" if 200 <= response.status_code < 300 else "unhealthy"
            return (
                f"Health Check Results:\n"
                f"URL: {url}\n"
                f"Status Code: {response.status_code}\n"
                f"Healthy: {status}\n"
                f"Response Time: {response.elapsed.total_seconds():.2f}s"
            )
        except requests.exceptions.Timeout:
            return f"Error: Timeout while checking {url}"
        except requests.exceptions.RequestException as e:
            return f"Error checking {url}: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    
    else:
        return f"Error: Unknown tool '{tool_name}'"

# Endpoint MCP Principale
@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    """
    Endpoint principale MCP over HTTP
    Compatibile con il client HTTP ufficiale di Anthropic
    """
    try:
        method = request.method
        msg_id = request.id
        
        print(f"MCP Request: {method} (ID: {msg_id})")
        
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                        "resources": {},
                        "prompts": {},
                        "logging": {}
                    },
                    "serverInfo": {
                        "name": "http-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_server_info",
                            "description": "Get server information, status and configuration",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "calculate_operation",
                            "description": "Perform mathematical calculations (+, -, *, /)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "Math operation like '2+2', '10*5', '(3+4)/2'"
                                    }
                                },
                                "required": ["operation"]
                            }
                        },
                        {
                            "name": "format_text",
                            "description": "Format text in different styles",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "Text to format"
                                    },
                                    "style": {
                                        "type": "string",
                                        "enum": ["uppercase", "lowercase", "title", "capitalize"],
                                        "description": "Text formatting style",
                                        "default": "uppercase"
                                    }
                                },
                                "required": ["text"]
                            }
                        },
                        {
                            "name": "check_remote_health",
                            "description": "Check health and status of a remote URL",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "url": {
                                        "type": "string",
                                        "description": "URL to check (include http:// or https://)",
                                        "default": "https://httpbin.org/status/200"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
            
        elif method == "tools/call":
            tool_name = request.params.get("name", "")
            arguments = request.params.get("arguments", {})
            
            print(f"Executing tool: {tool_name} with args: {arguments}")
            
            result_text = execute_tool(tool_name, arguments)
            
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            }
            
        elif method == "notifications/initialized":
            # Semplicemente conferma
            response = {
                "jsonrpc": "2.0", 
                "id": msg_id,
                "result": {}
            }
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported MCP method: {method}"
            )
        
        print(f"MCP Response: {method} -> Success")
        return response
        
    except Exception as e:
        print(f"MCP Error: {e}")
        error_response = {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }
        return error_response

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

from fastapi.responses import HTMLResponse

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
