import socket

# Comandos do protocolo SASE
CMD_GEN_NORMAL = "GEN:N"
CMD_GEN_PRIORITY = "GEN:P"
CMD_ACK = "ACK"        # Formato: ACK:N1 ou ACK:P1
CMD_CALL = "CALL"      # Formato: CALL:Guiche_1
CMD_TICKET = "TICKET"  # Formato: TICKET:N1 ou TICKET:EMPTY
CMD_SUB_TV = "SUB_TV"  # Registrar TV para receber notificações
CMD_UPDATE = "UPDATE"  # Formato: UPDATE:N1:Guiche_1

DELIMITER = "\n"

def send_msg(sock: socket.socket, msg: str):
    """Envia uma mensagem no formato UTF-8 anexando o delimitador de fim de mensagem."""
    try:
        payload = (msg + DELIMITER).encode("utf-8")
        sock.sendall(payload)
        return True
    except socket.error:
        return False

def recv_msg(sock: socket.socket) -> str:
    """Lê bytes do socket até encontrar o delimitador, retornando a mensagem decodificada ou None em caso de desconexão."""
    data = bytearray()
    while True:
        try:
            chunk = sock.recv(1)
            if not chunk:
                return None  # Conexão fechada pelo outro lado
            if chunk == b'\n':
                break
            data.extend(chunk)
        except (socket.error, ConnectionResetError):
            return None  # Falha na conexão
    return data.decode("utf-8")
