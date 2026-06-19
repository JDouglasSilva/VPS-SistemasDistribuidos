import os

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def draw_dashboard(current_ticket: str, current_ta: str, history: list, status_message: str = None):
    clear_screen()
    print("\033[95m┌──────────────────────────────────────────────────┐\033[0m")
    print("\033[95m│\033[0m          \033[1;97mSASE - PAINEL DE VISUALIZAÇÃO (TV)\033[0m       \033[95m│\033[0m")
    print("\033[95m└──────────────────────────────────────────────────┘\033[0m")
    
    # Exibe status da conexão se houver
    if status_message:
        color = "\033[92m" if "Conectado" in status_message else "\033[93m"
        print(f" Status: {color}{status_message}\033[0m\n")
    else:
        print()

    # Painel principal da senha atual
    if current_ticket and current_ticket != "Nenhum":
        is_priority = current_ticket.startswith("P")
        color = "\033[93m" if is_priority else "\033[92m"
        tipo = "PRIORITÁRIO" if is_priority else "NORMAL"
        
        print(f"{color} ┌──────────────────────────────────────────────┐\033[0m")
        print(f"{color} │\033[0m               \033[1;5;97m*** CHAMADA ***\033[0m                {color}│\033[0m")
        print(f"{color} │                                              │\033[0m")
        print(f"{color} │\033[0m         SENHA: {color}\033[1;47m  {current_ticket:<6}  \033[0m                     {color}│\033[0m")
        print(f"{color} │                                              │\033[0m")
        print(f"{color} │\033[0m         LOCAL: \033[1;97m{current_ta:<30}\033[0m       {color}│\033[0m")
        print(f"{color} │         TIPO : \033[1;97m{tipo:<30}\033[0m       {color}│\033[0m")
        print(f"{color} └──────────────────────────────────────────────┘\033[0m")
    else:
        print(" ┌──────────────────────────────────────────────┐")
        print(" │                                              │")
        print(" │         AGUARDANDO PRÓXIMA CHAMADA...        │")
        print(" │                                              │")
        print(" └──────────────────────────────────────────────┘")
        
    # Histórico de Chamadas Anteriores
    print("\n\033[96m Últimas Chamadas:\033[0m")
    print("\033[90m ------------------------------------------------\033[0m")
    if not history:
        print("  (Nenhuma senha chamada ainda)")
    else:
        for idx, (t, ta) in enumerate(history, 1):
            is_p = t.startswith("P")
            t_color = "\033[93m" if is_p else "\033[92m"
            print(f"  {idx}. Senha: {t_color}\033[1m{t:<4}\033[0m no \033[97m{ta}\033[0m")
    print("\033[90m ------------------------------------------------\033[0m")
