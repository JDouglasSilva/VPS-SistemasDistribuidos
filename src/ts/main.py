import time
import sys
import os
# Adiciona o diretório raiz do projeto ao path do sistema para resolver os imports da pasta 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ts.modules import tui
from src.ts.modules.socket_client import request_new_ticket

def main():
    try:
        while True:
            tui.clear_screen()
            tui.draw_header()
            tui.draw_menu()
            
            opcao = input("\033[93mOpção > \033[0m").strip()
            
            if opcao == "1":
                print("\n[*] Solicitando senha Normal ao servidor...")
                ticket = request_new_ticket(is_priority=False)
                if ticket:
                    tui.draw_ticket_card(ticket)
                else:
                    tui.draw_error("Não foi possível conectar ao Servidor SASE.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == "2":
                print("\n[*] Solicitando senha Prioritária ao servidor...")
                ticket = request_new_ticket(is_priority=True)
                if ticket:
                    tui.draw_ticket_card(ticket)
                else:
                    tui.draw_error("Não foi possível conectar ao Servidor SASE.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == "3":
                print("\n[*] Fechando terminal de senhas...")
                break
            else:
                print("\n\033[91mOpção inválida! Tente novamente.\033[0m")
                time.sleep(1.5)
                
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Terminal encerrado.")
    sys.exit(0)

if __name__ == "__main__":
    main()
