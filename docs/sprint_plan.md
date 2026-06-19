# Plano de Sprints - Desenvolvimento do SASE

Para construir o projeto SASE de forma organizada, iterativa e segura, dividiremos o trabalho em **4 Sprints** lógicas. Cada sprint constrói uma fundação para a próxima.

---

## **Sprint 1: Fundamentos de Comunicação e Infraestrutura**
* **Objetivo:** Estabelecer a comunicação socket TCP básica e a estrutura de diretórios.
* **Tarefas:**
  1. Criar a estrutura física de pastas do projeto (`src/srv`, `src/ts`, `src/ta`, `src/tv`, `src/shared`).
  2. Implementar `src/shared/config.py` com as configurações de porta/IP padrão.
  3. Implementar `src/shared/protocols.py` para padronizar os cabeçalhos e payloads das mensagens TCP.
  4. Desenvolver o esqueleto do Servidor TCP concorrente (`src/srv/modules/socket_server.py`) que aceita múltiplas conexões e cria threads para tratá-las.
* **Critério de Aceitação:** O servidor deve rodar, aceitar múltiplos clientes simultaneamente e imprimir logs simples de conexão/desconexão.

---

## **Sprint 2: Regras de Negócio e Geração de Senhas (SRV + TS)**
* **Objetivo:** Implementar o gerenciamento de filas no Servidor e a geração de senhas no Terminal de Senhas.
* **Tarefas:**
  1. Implementar o gerenciador de filas do servidor (`src/srv/modules/queue_manager.py`) com:
     - Mutexes (`threading.Lock`) para segurança de threads.
     - Filas de senhas normais e prioritárias.
     - A lógica de escalonamento: prioridade garantida após 2 normais consecutivas (`2N -> 1P`).
  2. Desenvolver a lógica de socket cliente do TS (`src/ts/modules/socket_client.py`) para enviar solicitações de novas senhas (`GEN:N` e `GEN:P`).
  3. Implementar o arquivo principal `src/ts/main.py` e um esqueleto interativo para o usuário.
* **Critério de Aceitação:** O usuário consegue gerar senhas pelo TS, o servidor as recebe, insere na fila correta de forma ordenada e imprime logs detalhados com timestamps das entradas.

---

## **Sprint 3: Chamada de Atendimento e Broadcast (TA + TV)**
* **Objetivo:** Permitir que guichês chamem as senhas e a TV atualize em tempo real via broadcast.
* **Tarefas:**
  1. Desenvolver a lógica de rede do TA (`src/ta/modules/socket_client.py`) para se conectar ao servidor e enviar o comando `CALL`.
  2. Atualizar o Servidor para realizar o processamento da regra de negócio `2N -> 1P` ao receber um `CALL`, retornando a senha certa para o TA.
  3. Desenvolver a lógica da TV (`src/tv/modules/socket_client.py`) para registrar-se no servidor via `SUB_TV` e ficar aguardando mensagens de `UPDATE` via conexão persistente.
  4. Implementar a lógica de broadcast no Servidor para notificar todas as TVs ativas quando uma senha for chamada.
* **Critério de Aceitação:** O atendente (TA) consegue chamar uma senha, o servidor seleciona a senha correta (respeitando a regra 2N->1P), envia-a para o TA correspondente e dispara um broadcast automático atualizando todas as TVs conectadas.

---

## **Sprint 4: Interface Rica no Terminal (TUI) e Documentação**
* **Objetivo:** Polimento visual das telas de console e elaboração do relatório técnico de entrega.
* **Tarefas:**
  1. Implementar `tui.py` para todos os módulos clientes:
     - **TS:** Tela limpa mostrando botões e o ticket gerado em destaque.
     - **TA:** Painel para o atendente ver o status e a senha atual.
     - **TV:** Tela em destaque gigante (com caracteres grandes e histórico formatado) para os clientes acompanharem, incluindo alerta sonoro de campainha terminal (`\a`).
  2. Criar o script utilitário `run_all.sh` para iniciar todos os terminais rapidamente para testes.
  3. Criar o relatório técnico final (`docs/relatorio.md`) com a identificação dos autores, diagramas de arquitetura, protocolo detalhado e manual de uso do sistema.
* **Critério de Aceitação:** Sistema funcionando de ponta a ponta com interfaces ricas, sem quebras de layout, com tratamento de exceções (como perda de conexão com o servidor) e documentação completa pronta para entrega.
