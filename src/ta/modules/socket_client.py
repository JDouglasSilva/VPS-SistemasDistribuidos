import socket
from src.shared.config import HOST, PORT
from src.shared import protocols

def call_next_ticket(ta_id: str) -> str:
    """Abre uma conexão temporária com o servidor, solicita o próximo atendimento e retorna a senha."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((HOST, PORT))
        
        # Comando: CALL:<TA_ID>
        cmd = f"{protocols.CMD_CALL}:{ta_id}"
        
        if protocols.send_msg(sock, cmd):
            resp = protocols.recv_msg(sock)
            if resp and resp.startswith(protocols.CMD_TICKET):
                # Formato: TICKET:N1 ou TICKET:EMPTY
                parts = resp.split(":")
                if len(parts) > 1:
                    ticket = parts[1]
                    if ticket == "EMPTY":
                        return "EMPTY"
                    return ticket
        return None
    except (socket.error, socket.timeout):
        return None
    finally:
        try:
            sock.close()
        except Exception:
            pass
