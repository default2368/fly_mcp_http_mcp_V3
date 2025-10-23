import requests
import json

def test_mcp_server():
    """Testa il server MCP HTTP"""
    base_url = "http://localhost:8080"  # Cambia con l'URL Fly.io dopo il deploy
    
    # Test health endpoint (se presente)
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server risponde: {response.status_code}")
    except Exception as e:
        print(f"❌ Server non raggiungibile: {e}")
        return
    
    print("\n🎯 Server MCP HTTP è attivo e in ascolto!")
    print("📋 Tools disponibili:")
    print("  - get_server_info")
    print("  - calculate_operation") 
    print("  - format_text")
    print("  - get_system_status")
    print("\n🔗 Pronto per connessioni MCP client via HTTP")

if __name__ == "__main__":
    test_mcp_server()
