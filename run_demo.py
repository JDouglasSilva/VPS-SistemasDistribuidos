import sys
import os
import time
import subprocess

# Adiciona a raiz do projeto ao path do sistema para resolver os pacotes da pasta 'src'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ts.modules.socket_client import request_new_ticket
from src.ta.modules.socket_client import call_next_ticket

def clean_up(server_proc, tv_proc):
    """Encerra os processos do servidor e do painel de TV de forma limpa."""
    print("\n\033[90m[*] Limpando processos da simulação...\033[0m")
    if server_proc:
        try:
            # Envia sinal de encerramento para o input do servidor para sair de forma graciosa
            server_proc.communicate(input="sair\n", timeout=2)
        except Exception:
            server_proc.kill()
            
    if tv_proc:
        try:
            tv_proc.terminate()
        except Exception:
            pass
    print("\033[92m[+] Processos encerrados.\033[0m")

def main():
    print("\033[2J\033[H", end="")
    print("\033[95m==================================================\033[0m")
    print("\033[95m          SASE - SCRIPT DE APRESENTAÇÃO          \033[0m")
    print("\033[95m==================================================\033[0m")
    print("Este script irá iniciar o servidor e a TV automaticamente,")
    print("e simular a geração e a chamada de senhas via rede.\n")
    
    server_process = None
    tv_process = None
    
    try:
        # 1. Iniciar o Servidor
        print("\033[94m[1/4] Iniciando o Servidor Central (SRV) em segundo plano...\033[0m")
        server_log = open("server_demo.log", "w", encoding="utf-8")
        server_process = subprocess.Popen(
            [sys.executable, "src/srv/main.py"],
            stdin=subprocess.PIPE,
            stdout=server_log,
            stderr=server_log,
            text=True
        )
        time.sleep(1.5)  # Espera o socket ligar
        
        # 2. Iniciar a TV
        print("\033[94m[2/4] Abrindo o Painel de Visualização (TV) em um terminal gráfico...\033[0m")
        # Tenta detectar um emulador de terminal para abrir a TV em primeiro plano
        if os.system("which gnome-terminal > /dev/null 2>&1") == 0:
            tv_process = subprocess.Popen(["gnome-terminal", "--title=SASE - Painel TV (APRESENTAÇÃO)", "--", sys.executable, "src/tv/main.py"])
        elif os.system("which konsole > /dev/null 2>&1") == 0:
            tv_process = subprocess.Popen(["konsole", "--new-tab", "-e", sys.executable, "src/tv/main.py"])
        elif os.system("which xterm > /dev/null 2>&1") == 0:
            tv_process = subprocess.Popen(["xterm", "-title", "SASE - Painel TV (APRESENTAÇÃO)", "-e", sys.executable, "src/tv/main.py"])
        else:
            print("\033[93m[AVISO] Nenhum emulador gráfico encontrado. O painel da TV rodará em segundo plano.\033[0m")
            tv_process = subprocess.Popen([sys.executable, "src/tv/main.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        time.sleep(2.0)  # Espera a TV se conectar ao Servidor
        
        # 3. Simular a geração de senhas no TS
        print("\n\033[94m[3/4] Gerando senhas no Terminal de Senhas (TS) via Sockets TCP...\033[0m")
        senhas = []
        # Fluxo de criação: Normal (N1), Normal (N2), Prioritário (P1), Normal (N3)
        fluxo_geracao = [
            ("Normal", False),
            ("Normal", False),
            ("Prioritário", True),
            ("Normal", False)
        ]
        
        for tipo, is_priority in fluxo_geracao:
            ticket = request_new_ticket(is_priority)
            if ticket:
                senhas.append(ticket)
                print(f"  \033[92m[TS -> SRV]\033[0m Senha \033[1m{ticket}\033[0m ({tipo}) gerada com sucesso.")
            else:
                print("  \033[91m[ERRO]\033[0m Falha ao gerar senha.")
            time.sleep(0.5)
            
        print(f"\nSenhas registradas no Servidor: \033[97m{senhas}\033[0m")
        time.sleep(1.0)
        
        # 4. Simular o atendimento nos guichês
        print("\n\033[94m[4/4] Simulando chamada de atendimentos no Terminal (TA)...\033[0m")
        print("Acompanhe as atualizações em tempo real no painel da TV aberta.\n")
        
        # Chamada 1: Deve ser N1
        print("\033[96m[Guichê 1]\033[0m Chamando próximo...")
        ticket = call_next_ticket("Guichê 1")
        print(f"  <- \033[92m[SRV -> TA]\033[0m Recebida senha: \033[1m{ticket}\033[0m no Guichê 1 (Esperado: N1)")
        time.sleep(3.5)
        
        # Chamada 2: Deve ser N2
        print("\033[96m[Guichê 2]\033[0m Chamando próximo...")
        ticket = call_next_ticket("Guichê 2")
        print(f"  <- \033[92m[SRV -> TA]\033[0m Recebida senha: \033[1m{ticket}\033[0m no Guichê 2 (Esperado: N2)")
        time.sleep(3.5)
        
        # Chamada 3: Regra especial ativa! Foram chamadas 2 normais consecutivas, havendo prioritária na fila (P1), ela DEVE ser chamada
        print("\033[96m[Guichê 1]\033[0m Chamando próximo...")
        print("\033[93m[INFO] Regra 2N -> 1P deve forçar a chamada da senha prioritária agora...\033[0m")
        ticket = call_next_ticket("Guichê 1")
        print(f"  <- \033[92m[SRV -> TA]\033[0m Recebida senha: \033[1m{ticket}\033[0m no Guichê 1 (Esperado: P1)")
        time.sleep(3.5)
        
        # Chamada 4: Deve ser N3
        print("\033[96m[Guichê 2]\033[0m Chamando próximo...")
        ticket = call_next_ticket("Guichê 2")
        print(f"  <- \033[92m[SRV -> TA]\033[0m Recebida senha: \033[1m{ticket}\033[0m no Guichê 2 (Esperado: N3)")
        time.sleep(3.0)
        
        print("\n\033[92m[+] Apresentação de fluxo finalizada com sucesso!\033[0m")
        
    except KeyboardInterrupt:
        print("\n\033[91m[-] Simulação interrompida pelo usuário.\033[0m")
    finally:
        clean_up(server_process, tv_process)
        try:
            server_log.close()
        except Exception:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()
