import subprocess
import time
import sys
import os
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ts.modules.socket_client import request_new_ticket
from src.shared.config import HOST, PORT

print("Iniciando o servidor em background...")
server_log = open("server_test.log", "w", encoding="utf-8")
server_process = subprocess.Popen(
    [sys.executable, "src/srv/main.py"],
    stdin=subprocess.PIPE,
    stdout=server_log,
    stderr=server_log,
    text=True
)
time.sleep(2.0)

print(f"Verificando se porta {PORT} está aberta...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    sock.connect((HOST, PORT))
    print("[+] Porta conectada com sucesso no teste direto!")
    sock.close()
except Exception as e:
    print(f"[-] Erro ao conectar na porta: {e}")

print("Chamando request_new_ticket...")
try:
    # Vamos re-implementar aqui temporariamente com prints para capturar a exceção exata
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((HOST, PORT))
    print("[+] Cliente conectou.")
    from src.shared import protocols
    cmd = protocols.CMD_GEN_NORMAL
    print(f"Enviando comando: {cmd}")
    protocols.send_msg(sock, cmd)
    print("Aguardando resposta...")
    resp = protocols.recv_msg(sock)
    print(f"Resposta recebida: {resp}")
    sock.close()
except Exception as e:
    print(f"[-] Exceção durante request_new_ticket: {type(e).__name__}: {e}")

server_process.terminate()
server_log.close()
