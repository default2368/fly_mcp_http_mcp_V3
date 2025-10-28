"""
MCP Dispatcher Module
Coordina tutti i moduli MCP
"""
import json
import requests
from typing import Dict, Any

try:
    from modules.mcp_tests import MCPMethods
    from modules.mcp_github import MCPGitHub
except ImportError:
    try:
        from .mcp_tests import MCPMethods
        from .mcp_github import MCPGitHub
    except ImportError:
        from mcp_tests import MCPMethods
        from mcp_github import MCPGitHub


class MCPDispatcher:
    """Dispatcher principale per tutti i tool MCP"""
    
    @staticmethod
    def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
        """Esegue il tool tramite il modulo appropriato"""
        
        # Tools del core
        if tool_name in [
            "get_server_info", "calculate_operation", "format_text", 
            "check_remote_health", "get_weather", "get_weather_dynamic"
        ]:
            return MCPMethods.execute_tool(tool_name, arguments)
        
        # Tools GitHub
        elif tool_name in [
            "get_github_repo_info", "get_github_user_info", "search_github_repos"
        ]:
            return MCPGitHub.execute_github_tool(tool_name, arguments)
        
        else:
            return f"Error: Unknown tool '{tool_name}'"

    @staticmethod
    def get_all_tools_list() -> list:
        """Combina tutte le liste di tools"""
        try:
            core_tools = MCPMethods.get_tools_list()
            github_tools = MCPGitHub.get_github_tools_list()
            return core_tools + github_tools
        except Exception as e:
            print(f"Error getting tools list: {e}")
            # Fallback ai tools core
            return MCPMethods.get_tools_list()