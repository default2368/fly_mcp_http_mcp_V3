"""
MCP Routes Module
Contiene gli endpoint API per il protocollo MCP
"""
from fastapi import HTTPException
from typing import Dict, Any
from modules.mcp_methods import MCPMethods


class MCPRoutes:
    """Classe per gestire le routes MCP"""
    
    @staticmethod
    async def handle_mcp_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gestisce le richieste MCP over HTTP
        Compatibile con il client HTTP ufficiale di Anthropic
        """
        try:
            method = request_data.get("method")
            msg_id = request_data.get("id")
            
            print(f"MCP Request: {method} (ID: {msg_id})")
            
            if method == "initialize":
                response = MCPMethods.handle_initialize(msg_id)
                
            elif method == "tools/list":
                response = MCPMethods.handle_tools_list(msg_id)
                
            elif method == "tools/call":
                params = request_data.get("params", {})
                response = MCPMethods.handle_tools_call(msg_id, params)
                
            elif method == "notifications/initialized":
                response = MCPMethods.handle_initialized_notification(msg_id)
                
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
                "id": request_data.get("id"),
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
            return error_response
