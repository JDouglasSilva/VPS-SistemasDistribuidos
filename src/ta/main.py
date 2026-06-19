import time
import sys
import os
# Adiciona o diretório raiz do projeto ao path do sistema para resolver os imports da pasta 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ta.modules import tui
from src.ta.modules.socket_client import call_next_ticket

def main():
    tui.clear_screen()
    print("\033[94m==================================================\033[0m")
    print("\033[94m        INICIALIZAÇÃO DO GUICHÊ DE ATENDIMENTO    \033[0m")
    print("\033[94m==================================================\033[0m")
    
    ta_id = input("\033[93mIdentificação do Guichê (ex: Guiche 1): \033[0m").strip()
    if not ta_id:
        ta_id = "Guiche_Generico"
        
    current_ticket = "Nenhum"
    msg_to_display = None
    is_err_msg = False
    
    try:
        while True:
            tui.clear_screen()
            tui.draw_header(ta_id)
            tui.draw_status(current_ticket)
            
            if msg_to_display:
                tui.draw_message(msg_to_display, is_err_msg)
                msg_to_display = None  # Reseta após exibir uma vez
                is_err_msg = False
                
            tui.draw_menu()
            
            opcao = input("\033[93mComando > \033[0m").strip()
            
            if opcao.lower() == "s":
                print("\n[*] Encerrando o guichê de atendimento...")
                break
            elif opcao == "":
                # Chamar próxima senha (pressionou Enter)
                print("\n[*] Solicitando próxima senha ao servidor...")
                ticket = call_next_ticket(ta_id)
                
                if ticket == "EMPTY":
                    current_ticket = "Nenhum"
                    msg_to_display = "Todas as filas estão vazias no momento."
                    is_err_msg = False
                elif ticket is None:
                    msg_to_display = "Não foi possível se conectar ao Servidor SASE."
                    is_err_msg = True
                else:
                    current_ticket = ticket
                    msg_to_display = f"Senha {ticket} chamada com sucesso!"
                    is_err_msg = False
            else:
                msg_to_display = "Opção inválida! Pressione Enter para chamar ou 's' para sair."
                is_err_msg = True
                time.sleep(1.0)
                
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Terminal encerrado.")
    sys.exit(0)

if __name__ == "__main__":
    main()
