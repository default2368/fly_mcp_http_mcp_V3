"""
Configuration for Unified MCP Server
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('MCP_PORT', 8080))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # MCP Server URL - per uso remoto
    MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://test-mcp-prodv1.fly.dev')
    
    # FastAPI Server URL 
    FASTAPI_SERVER_URL = os.getenv('FASTAPI_SERVER_URL', 'https://test-mcp-prodv1.fly.dev')
    
    # FastMPC Configuration
    FASTMPC_ENABLED = True
    FASTMPC_ENDPOINT = '/tools'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # CORS
    _allowed_origins = os.getenv('ALLOWED_ORIGINS', None)
    if _allowed_origins:
        ALLOWED_ORIGINS = _allowed_origins.split(',')
    else:
        ALLOWED_ORIGINS = [
            FASTAPI_SERVER_URL, 
            'https://test-mcp-prodv2.fly.dev',
            'http://localhost:3000',
            'http://127.0.0.1:3000'
        ]
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def to_dict(cls):
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'mcp_server_url': cls.MCP_SERVER_URL,
            'fastapi_server_url': cls.FASTAPI_SERVER_URL,
            'fastmpc_enabled': cls.FASTMPC_ENABLED,
            'allowed_origins': cls.ALLOWED_ORIGINS,
            'log_level': cls.LOG_LEVEL
        }

# Example usage:
if __name__ == "__main__":
    print("Current Configuration:")
    print(json.dumps(Config.to_dict(), indent=2))