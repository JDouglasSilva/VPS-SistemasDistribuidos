# Plano de Implementação - SASE (Modular)

Este plano descreve o projeto e a implementação de uma solução distribuída para gerenciamento de filas e atendimento por senha eletrônica utilizando **sockets TCP em Python**, organizada de forma modular para evitar arquivos extensos e facilitar a manutenção.

## Estrutura de Diretórios Proposta

O código do projeto será estruturado da seguinte forma:

```text
src/
├── srv/                   # SERVIDOR (SRV)
│   ├── main.py            # Inicializador do Servidor
│   └── modules/
│       ├── queue_manager.py # Lógica de filas (Normal, Prioridade e Regra 2N -> 1P)
│       └── socket_server.py # Gerenciamento de conexões TCP concorrentes (Threads)
│
├── ts/                    # TERMINAL DE SENHAS (TS)
│   ├── main.py            # Inicializador do Gerador de Senhas
│   └── modules/
│       ├── tui.py         # Interface de usuário (Terminal)
│       └── socket_client.py # Conexão e envio de senhas ao servidor
│
├── ta/                    # TERMINAL DE ATENDIMENTO (TA)
│   ├── main.py            # Inicializador do Guichê de Atendimento
│   └── modules/
│       ├── tui.py         # Interface de controle do operador
│       └── socket_client.py # Solicitação de senhas ao servidor
│
├── tv/                    # TERMINAL DE VISUALIZAÇÃO (TV)
│   ├── main.py            # Inicializador do Painel da TV
│   └── modules/
│       ├── tui.py         # Tela de exibição de senhas chamada
│       └── socket_client.py # Conexão persistente para broadcast em tempo real
│
└── shared/                # RECURSOS COMPARTILHADOS
    ├── __init__.py
    ├── config.py          # Configurações de Rede (IP, Porta, etc.)
    └── protocols.py       # Padrão de mensagens e serialização
```

---

## Arquitetura e Fluxo de Dados

1. **Protocolo de Mensagens (`shared/protocols.py`):**
   Definirá as constantes de comandos de forma padronizada. Todas as trocas de mensagens via socket seguirão o formato textual UTF-8 estruturado:
   - `GEN:N` / `GEN:P` -> Gerar senhas do TS para o Servidor.
   - `ACK:N<num>` / `ACK:P<num>` -> Confirmação do Servidor para o TS.
   - `CALL:<TA_ID>` -> Chamada de senha do TA para o Servidor.
   - `TICKET:<senha>` / `EMPTY` -> Resposta do Servidor para o TA.
   - `SUB_TV` -> Inscrição da TV para atualizações.
   - `UPDATE:<senha>:<TA_ID>` -> Broadcast do Servidor para todas as TVs.

2. **Lógica de Escalonamento de Filas (`srv/modules/queue_manager.py`):**
   O gerenciador de filas encapsulará o estado usando um `threading.Lock` para garantir exclusão mútua. A regra central de negócio será implementada assim:
   - Mantemos `normal_queue` e `priority_queue`.
   - Mantemos o contador `consecutive_normal_served`.
   - Se `consecutive_normal_served >= 2` e `priority_queue` não estiver vazia:
     - Removemos a senha da fila de prioridade (`priority_queue.pop(0)`).
     - Zeramos o contador `consecutive_normal_served`.
   - Caso contrário:
     - Se `normal_queue` não estiver vazia:
       - Removemos a senha da fila normal (`normal_queue.pop(0)`).
       - Incrementamos `consecutive_normal_served += 1`.
     - Caso contrário, se `priority_queue` não estiver vazia:
       - Removemos da fila de prioridade.
       - Zeramos o contador.
     - Se ambas estiverem vazias, retorna `None`.

3. **Gerenciamento de Rede (`srv/modules/socket_server.py`):**
   - O servidor criará um socket TCP (`socket.SOCK_STREAM`) escutando as conexões.
   - Para cada cliente conectado, uma nova thread (`threading.Thread`) será disparada para tratar a requisição de forma não bloqueante.
   - O servidor manterá uma lista de sockets de TV ativos para disparar os pacotes de `UPDATE` (broadcast) toda vez que um atendimento for iniciado.

4. **Interface Visual (Módulos `tui.py`):**
   - Interfaces limpas, utilizando códigos de cores ANSI (ex: `\033[92m` para verde, `\033[91m` para vermelho, etc.).
   - Utilização de comandos de limpar a tela (`clear` ou `os.system('clear')`) para atualizar as visualizações de forma elegante, simulando um aplicativo real sem piscar a tela de forma incômoda.

---

## Verificação e Testes

- **Simulação Automatizada:** Um script para criar carga nas filas simulando a chegada assíncrona de dezenas de clientes e atendentes chamando em paralelo, para atestar que o Mutex e a regra de 2N -> 1P estão funcionando.
- **Testes Manuais de Execução:** Scripts para iniciar as abas no Linux e interagir com os terminais.
