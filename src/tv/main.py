import sys
import os
# Adiciona o diretório raiz do projeto ao path do sistema para resolver os imports da pasta 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.tv.modules import tui
from src.tv.modules.socket_client import listen_for_updates

def main():
    current_ticket = "Nenhum"
    current_ta = ""
    history = []
    status_msg = "Iniciando conexão..."
    
    tui.draw_dashboard(current_ticket, current_ta, history, status_msg)
    
    try:
        # Fica em loop consumindo o gerador de atualizações de rede
        for ticket, ta_id in listen_for_updates():
            if ticket == "SYSTEM":
                # Mensagens de status do cliente (conexão, reconexão)
                status_msg = ta_id
                tui.draw_dashboard(current_ticket, current_ta, history, status_msg)
            else:
                # Atualização real de senha chamada
                status_msg = "Conectado ao Servidor SASE."
                
                # Se tínhamos uma senha ativa, move para o histórico
                if current_ticket and current_ticket != "Nenhum":
                    history.insert(0, (current_ticket, current_ta))
                    if len(history) > 5:
                        history.pop()  # Mantém apenas as últimas 5 no painel
                
                current_ticket = ticket
                current_ta = ta_id
                
                # Emite o bipe sonoro de alerta no terminal
                print("\a", end="", flush=True)
                
                tui.draw_dashboard(current_ticket, current_ta, history, status_msg)
                
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Painel encerrado.")
    sys.exit(0)

if __name__ == "__main__":
    main()
