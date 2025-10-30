#!/bin/bash
###############################################################################
# Script di setup e avvio automatico per MCP Server
# Path: /Users/default/Sviluppo/python/proxy_server/setup_env.sh
# Da eseguire all'avvio del Mac
###############################################################################

# Configurazione
BASE_DIR="/Users/default/Sviluppo/python/proxy_server"
VENV_DIR="$BASE_DIR/venv"
PYTHON_VENV="$VENV_DIR/bin/python3"
PIP_VENV="$VENV_DIR/bin/pip"
MAIN_SCRIPT="$BASE_DIR/proxy_server.py"
REQUIREMENTS="$BASE_DIR/requirements.txt"
LOG_FILE="$BASE_DIR/startup.log"
PID_FILE="$BASE_DIR/server.pid"

# Funzione per logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Intestazione
log "=================================================="
log "🔧 Setup MCP Server Environment"
log "=================================================="

# Vai nella directory del progetto
cd "$BASE_DIR" || {
    log "❌ Errore: impossibile accedere a $BASE_DIR"
    exit 1
}
log "📁 Directory: $BASE_DIR"

# Verifica esistenza virtual environment
if [ ! -d "$VENV_DIR" ]; then
    log "❌ Virtual environment non trovato!"
    log "Creazione virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        log "✅ Virtual environment creato"
    else
        log "❌ Errore nella creazione del virtual environment"
        exit 1
    fi
else
    log "✅ Virtual environment trovato"
fi

# Attiva virtual environment
source "$VENV_DIR/bin/activate"
log "✅ Virtual environment attivato"

# Aggiorna pip
log "Aggiornamento pip..."
"$PIP_VENV" install --upgrade pip >> "$LOG_FILE" 2>&1

# Installa/aggiorna dipendenze
if [ -f "$REQUIREMENTS" ]; then
    log "📦 Installazione dipendenze da requirements.txt..."
    "$PIP_VENV" install -r "$REQUIREMENTS" >> "$LOG_FILE" 2>&1
    if [ $? -eq 0 ]; then
        log "✅ Dipendenze installate/aggiornate"
    else
        log "❌ Errore nell'installazione delle dipendenze"
        exit 1
    fi
else
    log "⚠️  File requirements.txt non trovato"
fi

# Verifica se il server è già in esecuzione
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        log "⚠️  Server già in esecuzione con PID: $OLD_PID"
        log "Terminazione processo esistente..."
        kill "$OLD_PID"
        sleep 2
    fi
    rm -f "$PID_FILE"
fi

# Avvia il server MCP in background
log "🚀 Avvio MCP Server..."
nohup "$PYTHON_VENV" "$MAIN_SCRIPT" >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Salva il PID
echo "$SERVER_PID" > "$PID_FILE"

# Attendi un attimo per verificare se parte correttamente
sleep 3

# Verifica che il processo sia ancora attivo
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    log "✅ Server avviato con successo! PID: $SERVER_PID"
    log "📄 PID salvato in: $PID_FILE"
    log "📋 Log disponibile in: $LOG_FILE"
    log "=================================================="
    exit 0
else
    log "❌ Server terminato immediatamente dopo l'avvio"
    log "Controlla i log per dettagli: $LOG_FILE"
    log "=================================================="
    exit 1
fi