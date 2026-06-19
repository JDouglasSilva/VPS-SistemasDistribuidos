# Relatório Técnico - Sistema de Atendimento por Senha Eletrônica (SASE)

**Disciplina:** Sistemas Distribuídos  
**Data:** 18 de Junho de 2026  
**Autores:**  
* [Inserir Nome do Autor 1]  
* [Inserir Nome do Autor 2]  

---

## 1. Introdução

Este relatório descreve o projeto e a implementação de um **Sistema de Atendimento por Senha Eletrônica (SASE)**. Trata-se de uma aplicação distribuída concebida para ordenar, gerenciar e otimizar as filas de atendimento público em ambientes comerciais, bancários ou de serviços públicos. 

O objetivo do sistema é permitir que:
1. Senhas sejam emitidas de maneira distribuída em terminais de autoatendimento.
2. Atendentes em diferentes guichês chamem os clientes de forma sincronizada.
3. Um painel central (TV) notifique os clientes de forma instantânea sobre as chamadas.
4. Um servidor central coordene o estado do sistema de forma segura contra concorrência.

---

## 2. Soluções de Software Adotadas

Abaixo estão descritas as escolhas tecnológicas e arquiteturais feitas durante a concepção do SASE:

### 2.1. Linguagem de Programação
Optou-se pelo uso de **Python 3**. A linguagem oferece suporte nativo de alto nível a sockets de rede, primitivas de concorrência (threads e travas) e facilidade de depuração, sendo ideal para modelagem de sistemas distribuídos educacionais e de produção rápida.

### 2.2. Protocolo de Comunicação e Socket TCP
Para a comunicação entre os nós, utilizou-se sockets TCP orientados à conexão (`socket.SOCK_STREAM`). O TCP garante a entrega ordenada e confiável dos pacotes na rede.  
Para solucionar o problema clássico de fragmentação em sockets TCP (onde dados enviados consecutivamente podem se fundir em um único recebimento), desenhou-se um protocolo de delimitação simples:
* Toda mensagem é uma string codificada em **UTF-8**.
* Cada mensagem termina estritamente com o caractere delimitador `\n` (quebra de linha).
* O receptor lê byte a byte até detectar o `\n`, garantindo o isolamento perfeito de cada comando.

### 2.3. Concorrência no Servidor (Multi-threading)
Como o Servidor (SRV) centraliza múltiplos terminais que podem enviar e solicitar dados a qualquer instante, adotou-se o modelo **Thread-per-Client**:
* A thread principal do servidor escuta na porta TCP `5000`.
* A cada nova conexão aceita, uma thread de segundo plano (`threading.Thread`) é despachada para tratar aquele cliente.
* O encerramento ou travamento de uma conexão de terminal não afeta os demais terminais ativos.

### 2.4. Sincronização de Filas (Mutex)
As filas de atendimento são recursos compartilhados por todas as threads de conexão. Para evitar condições de corrida (por exemplo, dois guichês chamarem e receberem a mesma senha ao mesmo tempo), a manipulação das listas é protegida por uma exclusão mútua (*Mutex*), implementada através de `threading.Lock`. Toda leitura ou modificação das filas de senhas ocorre dentro de seções críticas protegidas pela trava.

---

## 3. Detalhamento dos Módulos e Funções

O sistema foi estruturado de forma modular na pasta `src/`:

### 3.1. Módulo Compartilhado (`src/shared/`)
* **`config.py`:** Concentra os parâmetros globais de rede (IP e Porta), facilitando migrações de servidor.
* **`protocols.py`:** Define os comandos de texto padrões (`GEN:N`, `GEN:P`, `CALL`, `UPDATE`, etc.) e implementa as funções utilitárias `send_msg()` e `recv_msg()`, blindando o restante da aplicação contra as complexidades de manipulação direta de buffers de sockets.

### 3.2. Servidor (`src/srv/`)
* **`queue_manager.py`:** Contém a classe `QueueManager`, responsável pela lógica interna do estado das filas.
  * `generate_ticket(is_priority)`: Insere uma senha ordenada na lista Normal ou Prioritária correspondente e gera o log com timestamp.
  * `call_ticket(ta_id)`: Aplica o algoritmo de escalonamento. A regra especial exige que **a cada duas senhas normais (N) chamadas consecutivamente, a próxima senha deve ser prioritária (P), se houver**. Se a fila P estiver vazia, o fluxo continua com as normais e vice-versa.
* **`socket_server.py`:** Implementa a classe `SaseSocketServer`. Controla o ciclo de vida do socket servidor, mantém a lista de conexões de TVs ativas e despacha o sinal de `UPDATE` via broadcast.

### 3.3. Terminal de Senhas (`src/ts/`)
* **`socket_client.py`:** Estabelece conexão com o servidor de forma temporária, envia o comando `GEN:N` ou `GEN:P` e espera o `ACK` de confirmação contendo a senha emitida.
* **`tui.py`:** Desenha o painel gráfico interativo do emissor no terminal.

### 3.4. Terminal de Atendimento (`src/ta/`)
* **`socket_client.py`:** Conecta ao servidor e envia o sinal `CALL:<guiche_id>`, recebendo de volta a senha selecionada ou uma mensagem de fila vazia.
* **`tui.py`:** Exibe uma interface confortável para o operador, exibindo o cliente em atendimento e permitindo novas chamadas por teclado de forma rápida.

### 3.5. Terminal de Visualização (`src/tv/`)
* **`socket_client.py`:** Estabelece uma conexão de rede persistente. Ao conectar-se, registra-se via `SUB_TV` e entra em bloqueio de escuta de mensagens. Possui um algoritmo de **reconexão automática com backoff** que impede que a queda do servidor trave a exibição da TV permanentemente.
* **`tui.py`:** Exibe o painel de atendimento clássico de salas de espera, destacando a última senha em tamanho expandido e listando o histórico das cinco últimas senhas chamadas.

---

## 4. Recursos de Interface (TUI)

Para prover uma experiência visual agradável sem a necessidade de dependências pesadas de ambiente de janelas X11 ou Wayland, o SASE utiliza **TUI (Text User Interface)** construída com sequências de escape ANSI:
* **Cores de Estado:** Verde (`\033[92m`) para senhas Normais e operações normais, Amarelo/Laranja (`\033[93m`) para senhas Prioritárias, Azul (`\033[94m`) para guichês e Vermelho (`\033[91m`) para erros e alertas.
* **Limpeza e Redesenho:** Telas são limpas usando o comando `clear` integrado a cada atualização de frame, evitando poluição de logs e simulando uma tela dinâmica estática de painéis comerciais.
* **Sinalização Sonora:** Emissão do caractere ASCII Bell (`\a`), o qual aciona o alto-falante padrão da placa-mãe ou do emulador de terminal sempre que um novo atendimento é disparado, chamando a atenção do público presente de forma idêntica a um estabelecimento físico.

---

## 5. Simulação e Apresentação Automatizada

Como facilitador para apresentações acadêmicas e validações rápidas de funcionamento do sistema distribuído, desenvolveu-se o arquivo `run_demo.py` na raiz do projeto. 

Esse script atua como um coordenador de demonstração que:
1. Inicia o processo do Servidor (`src/srv/main.py`) em segundo plano.
2. Abre a interface do Painel da TV (`src/tv/main.py`) em uma nova janela gráfica de terminal para visibilidade.
3. Importa e utiliza as bibliotecas clientes de rede do próprio projeto (`socket_client.py`) para emitir comandos programaticamente de forma sequencial (ex: gera `N1`, `N2`, `P1`, `N3` e em seguida realiza a chamada das senhas simulação guichês).
4. Comprova de forma autônoma a ordenação de fila, a regra de priorização especial `2N -> 1P` e a atualização instantânea por broadcast de rede na TV.
5. Finaliza graciosamente todos os subprocessos de segundo plano criados ao término da demonstração.

---

## 6. Conclusão

A implementação do SASE atende integralmente a todas as exigências do projeto, demonstrando de forma prática conceitos fundamentais de sistemas distribuídos, como comunicação por sockets de baixo nível, concorrência distribuída, exclusão mútua para consistência de dados, broadcast/multicast simulado de eventos em rede e persistência resiliente à falha.

