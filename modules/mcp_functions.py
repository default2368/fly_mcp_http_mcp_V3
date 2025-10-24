"""
MCP Methods Core Module
Contiene la logica principale dei metodi MCP
"""
import json
import requests
from typing import Dict, Any


class MCPMethods:
    """Classe principale per i metodi MCP"""
    
    @staticmethod
    def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
        """Esegue il tool specificato con gli argomenti forniti"""
        
        if tool_name == "get_server_info":
            return MCPMethods._get_server_info()
        
        elif tool_name == "calculate_operation":
            return MCPMethods._calculate_operation(arguments)
        
        elif tool_name == "format_text":
            return MCPMethods._format_text(arguments)
        
        elif tool_name == "check_remote_health":
            return MCPMethods._check_remote_health(arguments)
        
        else:
            return f"Error: Unknown tool '{tool_name}'"

    @staticmethod
    def _get_server_info() -> str:
        """Restituisce informazioni sul server"""
        return json.dumps({
            "server_name": "MCP HTTP Server",
            "version": "1.0.0",
            "status": "running",
            "protocol": "HTTP",
            "message": "Hello from Remote MCP Server!"
        }, indent=2)

    @staticmethod
    def _calculate_operation(arguments: Dict[str, Any]) -> str:
        """Esegue operazioni matematiche"""
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

    @staticmethod
    def _format_text(arguments: Dict[str, Any]) -> str:
        """Formatta il testo secondo lo stile specificato"""
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

    @staticmethod
    def _check_remote_health(arguments: Dict[str, Any]) -> str:
        """Controlla lo stato di un URL remoto"""
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

    @staticmethod
    def get_tools_list() -> list:
        """Restituisce la lista dei tools disponibili"""
        return [
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

    @staticmethod
    def handle_initialize(msg_id: int | str | None) -> dict:
        """Gestisce la richiesta di inizializzazione MCP"""
        return {
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

    @staticmethod
    def handle_tools_list(msg_id: int | str | None) -> dict:
        """Gestisce la richiesta di lista tools"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": MCPMethods.get_tools_list()
            }
        }

    @staticmethod
    def handle_tools_call(msg_id: int | str | None, params: Dict[str, Any]) -> dict:
        """Gestisce la chiamata a un tool"""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        print(f"Executing tool: {tool_name} with args: {arguments}")
        result_text = MCPMethods.execute_tool(tool_name, arguments)
        
        return {
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

    @staticmethod
    def handle_initialized_notification(msg_id: int | str | None) -> dict:
        """Gestisce la notifica di inizializzazione completata"""
        return {
            "jsonrpc": "2.0", 
            "id": msg_id,
            "result": {}
        }
