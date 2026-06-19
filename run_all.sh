#!/bin/bash

# Encontrar o comando do Python correto
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Define a raiz do projeto no PYTHONPATH para importações funcionarem corretamente
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH="$DIR"

echo "=================================================="
echo "          INICIALIZADOR AUTOMÁTICO SASE          "
echo "=================================================="
echo "Tentando detectar emulador de terminal para abrir os módulos..."

# Verificar se estamos usando gnome-terminal, konsole ou xterm
if command -v gnome-terminal &> /dev/null; then
    echo "[+] Detectado: gnome-terminal. Iniciando processos..."
    gnome-terminal --title="SASE - Servidor" -- bash -c "$PYTHON_CMD src/srv/main.py; exec bash"
    sleep 0.8
    gnome-terminal --title="SASE - TV" -- bash -c "$PYTHON_CMD src/tv/main.py; exec bash"
    sleep 0.8
    gnome-terminal --title="SASE - Terminal de Senhas" -- bash -c "$PYTHON_CMD src/ts/main.py; exec bash"
    sleep 0.8
    gnome-terminal --title="SASE - Terminal de Atendimento" -- bash -c "$PYTHON_CMD src/ta/main.py; exec bash"
    echo "[+] Terminais abertos com sucesso."
    
elif command -v konsole &> /dev/null; then
    echo "[+] Detectado: konsole. Iniciando abas..."
    konsole --new-tab -e "$PYTHON_CMD src/srv/main.py" &
    sleep 0.8
    konsole --new-tab -e "$PYTHON_CMD src/tv/main.py" &
    sleep 0.8
    konsole --new-tab -e "$PYTHON_CMD src/ts/main.py" &
    sleep 0.8
    konsole --new-tab -e "$PYTHON_CMD src/ta/main.py" &
    echo "[+] Terminais abertos com sucesso."
    
elif command -v xterm &> /dev/null; then
    echo "[+] Detectado: xterm. Iniciando janelas..."
    xterm -title "SASE - Servidor" -e "$PYTHON_CMD src/srv/main.py" &
    sleep 0.8
    xterm -title "SASE - TV" -e "$PYTHON_CMD src/tv/main.py" &
    sleep 0.8
    xterm -title "SASE - Terminal de Senhas" -e "$PYTHON_CMD src/ts/main.py" &
    sleep 0.8
    xterm -title "SASE - Terminal de Atendimento" -e "$PYTHON_CMD src/ta/main.py" &
    echo "[+] Terminais abertos com sucesso."
    
else
    echo "[-] Nenhum emulador gráfico compatível encontrado."
    echo "Por favor, abra manualmente 4 abas/janelas de terminal e execute:"
    echo ""
    echo "Aba 1 (Servidor):"
    echo "  export PYTHONPATH=$DIR && $PYTHON_CMD src/srv/main.py"
    echo ""
    echo "Aba 2 (TV):"
    echo "  export PYTHONPATH=$DIR && $PYTHON_CMD src/tv/main.py"
    echo ""
    echo "Aba 3 (Terminal de Senhas - TS):"
    echo "  export PYTHONPATH=$DIR && $PYTHON_CMD src/ts/main.py"
    echo ""
    echo "Aba 4 (Terminal de Atendimento - TA):"
    echo "  export PYTHONPATH=$DIR && $PYTHON_CMD src/ta/main.py"
fi
