import os

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def draw_header():
    print("\033[96m┌──────────────────────────────────────────────────┐\033[0m")
    print("\033[96m│\033[0m          \033[1;97mSASE - TERMINAL DE SENHAS (TS)\033[0m          \033[96m│\033[0m")
    print("\033[96m└──────────────────────────────────────────────────┘\033[0m")

def draw_menu():
    print("\nEscolha o tipo de senha desejada:")
    print("  [\033[92m 1 \033[0m] \033[1;92mSenha Normal (N)\033[0m")
    print("  [\033[93m 2 \033[0m] \033[1;93mSenha Prioritária (P)\033[0m")
    print("  [\033[91m 3 \033[0m] Sair do Terminal")
    print("\n----------------------------------------------------")

def draw_ticket_card(ticket: str):
    is_priority = ticket.startswith("P")
    color = "\033[93m" if is_priority else "\033[92m"
    tipo = "PRIORITÁRIO" if is_priority else "NORMAL"
    
    print(f"\n{color}┌──────────────────────────────────────────────────┐\033[0m")
    print(f"{color}│\033[0m               \033[1;97mSENHA GERADA COM SUCESSO\033[0m           {color}│\033[0m")
    print(f"{color}│                                                  │\033[0m")
    print(f"{color}│\033[0m                   {color}\033[1;5;47m  {ticket}  \033[0m                        {color}│\033[0m")
    print(f"{color}│                                                  │\033[0m")
    print(f"{color}│\033[0m              Tipo: \033[1;97m{tipo:<11}\033[0m                      {color}│\033[0m")
    print(f"{color}└──────────────────────────────────────────────────┘\033[0m")
    print("\nRetire a sua senha e aguarde a chamada no painel...")

def draw_error(msg: str):
    print(f"\n\033[91m[ERRO] {msg}\033[0m")
    print("Por favor, tente novamente mais tarde.")
