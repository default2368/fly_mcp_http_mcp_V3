# Flusso dell'Applicazione MCP

Ecco il flusso dettagliato dell'applicazione, dalla ricezione di una richiesta HTTP all'esecuzione del metodo MCP:

## 1. Ingresso della Richiesta (main.py)

```
HTTP Request → FastAPI Application → /mcp Endpoint
```

* La richiesta HTTP arriva all'endpoint `/mcp`
* FastAPI la instrada alla funzione `handle_mcp_request` in `main.py`

```python
# main.py
@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    """Endpoint principale MCP over HTTP"""
    return await MCPRoutes.handle_mcp_request(request.dict())
```

## 2. Gestione della Route (mcp_routes.py)

```
MCPRoutes.handle_mcp_request() → Gestione Metodo → Chiamata a MCPMethods
```

* La richiesta viene passata a `MCPRoutes.handle_mcp_request()`
* Viene estratto il metodo dalla richiesta (es: "tools/call")
* In base al metodo, viene chiamata la funzione appropriata in `MCPMethods`

```python
# routes/mcp_routes.py
if method == "tools/call":
    params = request_data.get("params", {})
    response = MCPMethods.handle_tools_call(msg_id, params)
```

## 3. Esecuzione del Tool (mcp_methods.py)

```
MCPMethods.handle_tools_call() → Esecuzione Tool Specifico → Risposta
```

* `handle_tools_call` riceve i parametri e identifica quale tool eseguire
* Chiama la funzione specifica del tool (es: `_format_text`)

```python
# modules/mcp_methods.py
@staticmethod
def handle_tools_call(msg_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    # Esegue il tool specifico
    result = MCPMethods.execute_tool(tool_name, arguments)
    
    # Costruisce la risposta JSON-RPC
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": result
    }

@staticmethod
def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    if tool_name == "format_text":
        return MCPMethods._format_text(arguments)
    # ... altri tools ...
```

## 4. Esecuzione del Tool Specifico (es: format_text)

```python
@staticmethod
def _format_text(arguments: Dict[str, Any]) -> str:
    text = arguments.get("text", "")
    style = arguments.get("style", "uppercase")
    
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
```

## 5. Ritorno della Risposta

Il flusso torna indietro attraverso i livelli:

1. Il tool restituisce il risultato a `execute_tool`
2. `execute_tool` restituisce a `handle_tools_call`
3. `handle_tools_call` impacchetta il risultato in formato JSON-RPC
4. La risposta viene restituita al client

## 6. Gestione degli Errori

Ogni livello gestisce i propri errori:

* FastAPI gestisce gli errori di validazione
* MCPRoutes gestisce i metodi non supportati
* MCPMethods gestisce gli errori specifici dei tool

## Diagramma del Flusso

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant MCPRoutes
    participant MCPMethods
    
    Client->>+FastAPI: POST /mcp
    FastAPI->>+MCPRoutes: handle_mcp_request()
    
    alt Metodo supportato
        MCPRoutes->>+MCPMethods: handle_tools_call()
        MCPMethods->>MCPMethods: execute_tool()
        MCPMethods->>MCPMethods: _format_text() o altro tool
        MCPMethods-->>MCPRoutes: Risultato
    else Metodo non supportato
        MCPRoutes-->>-FastAPI: Errore 400
    end
    
    MCPRoutes-->>-FastAPI: Risposta JSON-RPC
    FastAPI-->>-Client: HTTP 200 + Risposta
```

---

Questo flusso garantisce una chiara separazione delle responsabilità e rende l'applicazione facile da mantenere ed estendere con nuovi tool.
