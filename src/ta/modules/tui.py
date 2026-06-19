import os

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def draw_header(ta_id: str):
    print("\033[94m┌──────────────────────────────────────────────────┐\033[0m")
    print(f"\033[94m│\033[0m      \033[1;97mSASE - TERMINAL DE ATENDIMENTO (TA)\033[0m         \033[94m│\033[0m")
    print(f"\033[94m│\033[0m      Identificação: \033[1;93m{ta_id:<27}\033[0m       \033[94m│\033[0m")
    print("\033[94m└──────────────────────────────────────────────────┘\033[0m")

def draw_status(current_ticket: str):
    print("\nStatus de Atendimento Atual:")
    if current_ticket == "Nenhum" or not current_ticket:
        print("  \033[90m[ Ocioso - Sem cliente em atendimento ]\033[0m")
    else:
        is_priority = current_ticket.startswith("P")
        color = "\033[93m" if is_priority else "\033[92m"
        tipo = "Prioritário" if is_priority else "Normal"
        print(f"  Atendendo a senha: {color}\033[1;47m  {current_ticket}  \033[0m ({tipo})")

def draw_menu():
    print("\nComandos Disponíveis:")
    print("  [\033[92m Enter \033[0m] Chamar Próximo Cliente")
    print("  [\033[91m   s   \033[0m] Sair / Fechar Guichê")
    print("\n----------------------------------------------------")

def draw_message(msg: str, is_error: bool = False):
    color = "\033[91m" if is_error else "\033[93m"
    prefix = "[ERRO]" if is_error else "[AVISO]"
    print(f"\n{color}{prefix} {msg}\033[0m")
