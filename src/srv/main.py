import time
import sys
import os
# Adiciona o diretório raiz do projeto ao path do sistema para resolver os imports da pasta 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.srv.modules.queue_manager import QueueManager
from src.srv.modules.socket_server import SaseSocketServer

def main():
    print("\033[2J\033[H", end="")  # Limpa a tela
    print("\033[95m==================================================\033[0m")
    print("\033[95m          SASE - SERVIDOR CENTRAL (SRV)          \033[0m")
    print("\033[95m==================================================\033[0m")
    
    queue_manager = QueueManager()
    server = SaseSocketServer(queue_manager)
    server.start()
    
    print("\nDigite \033[96m'status'\033[0m para ver a situação das filas.")
    print("Digite \033[91m'sair'\033[0m para encerrar o servidor.\n")
    
    try:
        while True:
            try:
                cmd = input("\033[93mSRV > \033[0m").strip().lower()
            except EOFError:
                # Ocorre quando o stdin está fechado ou redirecionado (ex: subprocesso)
                # Mantém o servidor rodando em background sem travar o processamento de sockets
                while True:
                    time.sleep(10)
                    
            if cmd == "sair":
                print("[*] Encerrando o servidor...")
                server.stop()
                break
            elif cmd == "status":
                status = queue_manager.get_status()
                print("\033[94m--------------------------------------------------\033[0m")
                print(f" Senhas na Fila Normal ({status['normal_len']}): {status['normal_queue']}")
                print(f" Senhas na Fila Prioritária ({status['priority_len']}): {status['priority_queue']}")
                print(f" Atendimentos Normais Consecutivos: {status['consecutive_normal']}")
                print("\033[94m--------------------------------------------------\033[0m")
            elif cmd == "":
                continue
            else:
                print("[-] Comando não reconhecido. Use 'status' ou 'sair'.")
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Encerrando o servidor de forma forçada...")
        server.stop()
    
    print("[*] Servidor finalizado.")
    sys.exit(0)

if __name__ == "__main__":
    main()
