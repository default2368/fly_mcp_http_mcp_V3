#!/usr/bin/env python3
import sys
import json
import requests

REMOTE_SERVER = "https://fly-mcp-http-v3.fly.dev/mcp"

while True:
    line = sys.stdin.readline()
    if not line:
        break
    
    try:
        request = json.loads(line.strip())
        response = requests.post(REMOTE_SERVER, json=request, timeout=30)
        print(response.text, flush=True)
    except Exception as e:
        error = {
            "jsonrpc": "2.0",
            "id": request.get("id") if 'request' in locals() else None,
            "error": {"code": -32603, "message": str(e)}
        }
        print(json.dumps(error), flush=True)
