import socket
import time
from src.shared.config import HOST, PORT
from src.shared import protocols

def listen_for_updates():
    """Conecta ao servidor, registra-se como TV e entrega as atualizações de chamadas (yield).
       Se a conexão falhar ou cair, tenta reconectar automaticamente."""
    while True:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Para evitar que conexões persistentes fiquem travadas infinitamente sem detectar quedas de rede
            sock.settimeout(None) 
            sock.connect((HOST, PORT))
            
            # Envia o sinal de registro da TV
            if protocols.send_msg(sock, protocols.CMD_SUB_TV):
                yield ("SYSTEM", "Conectado ao Servidor SASE.")
                
                # Loop de recebimento de atualizações
                while True:
                    msg = protocols.recv_msg(sock)
                    if msg is None:
                        # Servidor desconectou
                        break
                    
                    parts = msg.split(":")
                    if parts[0] == protocols.CMD_UPDATE and len(parts) >= 3:
                        ticket = parts[1]
                        ta_id = parts[2]
                        yield (ticket, ta_id)
            
        except socket.error:
            yield ("SYSTEM", "Sem conexão. Tentando reconectar...")
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
        
        # Espera 3 segundos antes de tentar reconectar
        time.sleep(3)
