# Sistema de Atendimento por Senha Eletrônica (SASE)

Este projeto consiste de uma solução de software distribuído desenvolvida para gerenciar filas de atendimento de forma justa e organizada. Ele foi implementado utilizando **Sockets TCP** e **Threads concorrentes** em Python, com interfaces interativas no terminal.

## Arquitetura do Sistema

O projeto adota uma arquitetura Cliente-Servidor distribuída dividida em quatro partes principais:

1. **Servidor (SRV):** Atua como o nó coordenador central, contendo o estado das filas de senhas e a regra de priorização. Ele lida com conexões de rede em paralelo via threads e sincroniza o acesso às filas por exclusão mútua (*mutexes*).
2. **Terminal de Senhas (TS):** Terminal de entrada onde os clientes geram senhas do tipo Normal (N) ou Prioritário (P).
3. **Terminal de Atendimento (TA):** Computador do atendente nos guichês que solicita a próxima senha a ser atendida.
4. **Terminal de Visualização (TV):** Painel da sala de espera que recebe e mostra as senhas chamadas em tempo real (broadcast).

---

## Estrutura de Pastas

```text
├── docs/
│   ├── implementation_plan.md  # Plano técnico
│   ├── sprint_plan.md          # Divisão do trabalho
│   └── relatorio.md            # Relatório técnico final
├── src/
│   ├── srv/                    # Servidor
│   ├── ts/                     # Terminal de Senhas
│   ├── ta/                     # Terminal de Atendimento
│   ├── tv/                     # Terminal de Visualização
│   └── shared/                 # Código comum (Rede e Protocolo)
├── run_all.sh                  # Inicializador automático para Linux
└── README.md                   # Este manual
```

---

## Como Executar

### Pré-requisitos
* Python 3.x instalado no Linux.

### Execução Automática (Desktop Linux)
O projeto inclui um script utilitário que detecta o emulador de terminal do seu sistema (Gnome Terminal, Konsole, Xterm) e abre as 4 janelas/abas necessárias com um único comando:

```bash
./run_all.sh
```

### Apresentação Automatizada (Simulação / Demo)
Para realizar uma apresentação do fluxo completo de forma 100% automatizada (ideal para demonstrações em aula), execute o script:

```bash
python3 run_demo.py
```
Esse script subirá o servidor em segundo plano, abrirá a TV em um terminal gráfico e simulará a geração das senhas (`N1`, `N2`, `P1`, `N3`) e a chamada delas pelos guichês, comprovando a lógica de ordenação e a regra `2N -> 1P` de forma autônoma e interativa.


### Execução Manual (Aba por Aba)
Se você estiver rodando em ambiente sem interface gráfica ou queira iniciar manualmente, abra 4 abas no terminal e execute os seguintes comandos a partir da raiz do projeto:

1. **Aba 1 - Iniciar o Servidor (SRV):**
   ```bash
   export PYTHONPATH=. && python3 src/srv/main.py
   ```
2. **Aba 2 - Iniciar o Painel de Visualização (TV):**
   ```bash
   export PYTHONPATH=. && python3 src/tv/main.py
   ```
3. **Aba 3 - Iniciar o Terminal de Senhas (TS):**
   ```bash
   export PYTHONPATH=. && python3 src/ts/main.py
   ```
4. **Aba 4 - Iniciar o Terminal de Atendimento (TA):**
   ```bash
   export PYTHONPATH=. && python3 src/ta/main.py
   ```

*Nota: Você pode abrir múltiplos terminais de atendimento (TAs) para testar a distribuição de senhas entre diferentes guichês concorrentes.*

---

## Regra de Escalonamento (Negócio)
A fila é organizada de acordo com as seguintes regras de negócio implementadas no Servidor:
* **Fila Normal (N) e Prioritária (P):** Senhas geradas em ordens crescentes independentes (N1, N2, P1, P2...).
* **Regra Especial `2N -> 1P`:** Para garantir a priorização sem deixar a fila comum travada, a cada 2 senhas Normais atendidas consecutivamente, o Servidor é obrigado a enviar uma senha Prioritária (P) para o próximo guichê que chamar, desde que exista alguma senha prioritária na fila.
* Se não houver senhas prioritárias, o servidor continua chamando as normais normalmente (e vice-versa).

---

## Relatório Técnico

### Identificação
**Autores:** João Douglas da Silva Freitas e João Matheus Alves Costa
**Projeto:** Sistema de Atendimento por Senha Eletrônica (SASE)

### Detalhamento das Funções e Soluções de Software Adotadas
O projeto foi desenvolvido em **Python 3** e atende a todos os requisitos arquiteturais e funcionais propostos, utilizando a abordagem de sistemas distribuídos Cliente-Servidor.
A comunicação entre os nós ocorre de forma padronizada via **Sockets TCP/IP**, garantindo a entrega confiável das mensagens na rede de acordo com o protocolo definido.

1. **Servidor (SRV):** 
   - Implementado como um servidor socket multi-thread (uma thread dedicada por cliente conectado).
   - Gerencia as filas de senhas (Normal e Prioritária) utilizando `threading.Lock` para garantir exclusão mútua. Isso evita *race conditions* (condições de corrida) quando múltiplos Terminais de Senhas (TS) ou Terminais de Atendimento (TA) operam simultaneamente.
   - O servidor aplica a lógica estrita: a cada 2 senhas Normais (N) enviadas aos TAs, a próxima requisição deverá ser respondida obrigatoriamente com uma senha Prioritária (P), se esta houver na fila.
   - Emite logs com *timestamps* exatos no terminal para auditar o instante de geração, envio e recebimento de SEAs.
   - Possui lógica de *Broadcast* que distribui automaticamente a senha chamada para todos os painéis de visualização conectados.

2. **Terminal de Senhas (TS):**
   - Atua como cliente TCP de envio. Possui interface TUI que permite ao usuário escolher entre senha Normal (N) ou Prioritária (P).
   - O TS envia o comando para o Servidor e este retorna a senha gerada (e.g. N1, N2, P1, etc.), mantendo a consistência da sequência.

3. **Terminal de Atendimento (TA):**
   - Atua como cliente TCP operado pelo atendente do guichê. 
   - Envia solicitação de próxima senha ao Servidor, exibindo a SEA retornada e já validada, sendo esta proveniente da geração prévia no TS.

4. **Terminal de Visualização (TV):**
   - Opera como um cliente TCP de "escuta contínua". 
   - Ao iniciar, conecta-se e assina os eventos de broadcast do servidor. Exibe em formato destacado a exata senha que foi direcionada para atendimento em um TA.

### Recursos de Interface
Foram empregadas interfaces de terminal interativas (TUI) desenvolvidas no próprio Python. O painel da TV, a tela do TA e do TS contam com menus e visuais baseados em caracteres, colorização e limpezas de tela que simulam displays físicos (como monitores ou letreiros de LEDs comumente utilizados em painéis de atendimento).
