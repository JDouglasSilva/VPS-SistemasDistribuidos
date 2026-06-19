import socket
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.shared.config import HOST, PORT

print(f"Tentando conectar ao Servidor SASE em {HOST}:{PORT}...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    sock.connect((HOST, PORT))
    print("[+] Conectado com sucesso!")
    sock.close()
except Exception as e:
    print(f"[-] Erro ao conectar: {type(e).__name__}: {e}")
