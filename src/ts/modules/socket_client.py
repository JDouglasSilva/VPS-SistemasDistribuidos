import socket
from src.shared.config import HOST, PORT
from src.shared import protocols

def request_new_ticket(is_priority: bool) -> str:
    """Abre uma conexão temporária com o servidor, solicita a senha e a retorna."""
    try:
        # Cria o socket e conecta
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)  # Timeout de 5 segundos
        sock.connect((HOST, PORT))
        
        # Define o comando correspondente
        cmd = protocols.CMD_GEN_PRIORITY if is_priority else protocols.CMD_GEN_NORMAL
        
        # Envia e recebe
        if protocols.send_msg(sock, cmd):
            resp = protocols.recv_msg(sock)
            if resp and resp.startswith(protocols.CMD_ACK):
                # O formato esperado é ACK:N1 ou ACK:P1, pegamos apenas a senha
                parts = resp.split(":")
                if len(parts) > 1:
                    return parts[1]
        return None
    except (socket.error, socket.timeout):
        return None
    finally:
        try:
            sock.close()
        except Exception:
            pass
