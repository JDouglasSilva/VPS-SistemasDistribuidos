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
