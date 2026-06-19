import socket
import threading
from datetime import datetime
from src.shared.config import HOST, PORT
from src.shared import protocols
from src.srv.modules.queue_manager import QueueManager

class SaseSocketServer:
    def __init__(self, queue_manager: QueueManager):
        self.queue_manager = queue_manager
        self.tv_sockets = []
        self.tv_lock = threading.Lock()
        self.running = False
        self.server_socket = None

    def start(self):
        """Inicia o servidor de sockets TCP."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            self.running = True
            print(f"[*] Servidor SASE iniciado em {HOST}:{PORT}")
            
            # Thread para aceitar novas conexões
            accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
            accept_thread.start()
        except Exception as e:
            print(f"[-] Erro ao iniciar o servidor: {e}")

    def _accept_connections(self):
        """Loop contínuo aceitando conexões de clientes (TS, TA, TV)."""
        while self.running:
            try:
                client_sock, client_addr = self.server_socket.accept()
                # Cria uma thread para lidar com o cliente conectado
                client_thread = threading.Thread(
                    target=self._handle_client, 
                    args=(client_sock, client_addr), 
                    daemon=True
                )
                client_thread.start()
            except socket.error:
                break

    def _handle_client(self, sock: socket.socket, addr):
        """Trata as requisições de um cliente específico de forma assíncrona."""
        print(f"[*] [CONEXÃO] Cliente conectado a partir de {addr[0]}:{addr[1]}")
        is_tv = False
        try:
            while self.running:
                msg = protocols.recv_msg(sock)
                if msg is None:
                    # Conexão fechada pelo cliente
                    break
                
                parts = msg.split(":")
                cmd = parts[0]
                
                if msg == protocols.CMD_GEN_NORMAL:
                    # Gerar Senha Normal
                    ticket = self.queue_manager.generate_ticket(is_priority=False)
                    protocols.send_msg(sock, f"{protocols.CMD_ACK}:{ticket}")
                    
                elif msg == protocols.CMD_GEN_PRIORITY:
                    # Gerar Senha Prioritária
                    ticket = self.queue_manager.generate_ticket(is_priority=True)
                    protocols.send_msg(sock, f"{protocols.CMD_ACK}:{ticket}")
                    
                elif cmd == protocols.CMD_CALL:
                    # Chamar Senha (TA)
                    ta_id = parts[1] if len(parts) > 1 else "Guiche_Desconhecido"
                    ticket = self.queue_manager.call_ticket(ta_id)
                    
                    if ticket:
                        protocols.send_msg(sock, f"{protocols.CMD_TICKET}:{ticket}")
                        # Notifica instantaneamente todas as TVs (Broadcast)
                        self._broadcast_to_tvs(ticket, ta_id)
                    else:
                        protocols.send_msg(sock, f"{protocols.CMD_TICKET}:EMPTY")
                        
                elif cmd == protocols.CMD_SUB_TV:
                    # Registrar TV para Broadcast
                    is_tv = True
                    with self.tv_lock:
                        self.tv_sockets.append(sock)
                    # Mantém a conexão aberta esperando atualizações (não fechamos o socket)
                    # O loop continuará rodando para detectar desconexão da TV
                    continue
                    
        except Exception as e:
            pass
        finally:
            # Limpeza após desconexão
            if is_tv:
                with self.tv_lock:
                    if sock in self.tv_sockets:
                        self.tv_sockets.remove(sock)
            try:
                sock.close()
            except socket.error:
                pass

    def _broadcast_to_tvs(self, ticket: str, ta_id: str):
        """Envia a atualização de senha chamada para todos os painéis de TV conectados."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"{protocols.CMD_UPDATE}:{ticket}:{ta_id}"
        
        with self.tv_lock:
            # Lista temporária para sockets que falharem (desconectados)
            broken_sockets = []
            for tv_sock in self.tv_sockets:
                success = protocols.send_msg(tv_sock, msg)
                if not success:
                    broken_sockets.append(tv_sock)
            
            # Limpa conexões inativas
            for bad_sock in broken_sockets:
                if bad_sock in self.tv_sockets:
                    self.tv_sockets.remove(bad_sock)
                    try:
                        bad_sock.close()
                    except socket.error:
                        pass
        
        # Log exigido na especificação: "Informar o instante em que enviou uma SEA para TA e TV."
        print(f"[{timestamp}] [BROADCAST] Notificação da senha {ticket} enviada para as TVs conectadas.")

    def stop(self):
        """Para o servidor de forma limpa."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except socket.error:
                pass
            
        with self.tv_lock:
            for sock in self.tv_sockets:
                try:
                    sock.close()
                except socket.error:
                    pass
            self.tv_sockets.clear()
