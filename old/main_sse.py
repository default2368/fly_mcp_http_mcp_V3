"""
MCP Server for Claude MCP integration using stdio.
This service communicates with Claude using the MCP protocol over stdio.
"""
import json
import sys
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator

def initialize_response(request_id: Optional[str] = None) -> Dict[str, Any]:
    """Generate initialization response for MCP protocol"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "claude-mcp-local",
                "version": "1.0.0"
            }
        }
    }

async def handle_mcp_requests():
    """Handle MCP protocol messages over stdio"""
    while True:
        # Read a line from stdin
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
            
        try:
            request = json.loads(line)
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                response = initialize_response(request_id)
                print(json.dumps(response), flush=True)
                
            # Add more MCP method handlers here
            
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if isinstance(request, dict) else None,
                "error": {"code": -32700, "message": "Parse error"}
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if isinstance(request, dict) else None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    # Set up asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the MCP server
        loop.run_until_complete(handle_mcp_requests())
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        loop.close()
