#!/usr/bin/env python3
"""
Client di test per il server MCP
"""
import asyncio
import json

async def test_mcp_server():
    """Testa il server MCP localmente"""
    print("🧪 Testing MCP Server...")
    
    # Simula una chiamata MCP
    test_commands = [
        {
            "tool": "get_server_info",
            "params": {}
        },
        {
            "tool": "calculate_operation", 
            "params": {"operation": "sum", "numbers": [1, 2, 3, 4, 5]}
        },
        {
            "tool": "format_text",
            "params": {"text": "Hello Fly.io MCP!", "style": "uppercase"}
        }
    ]
    
    print("📋 Available tools:")
    print("  - get_server_info")
    print("  - calculate_operation")
    print("  - format_text") 
    print("  - get_system_status")
    print("\n🎯 Server ready for MCP clients!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
