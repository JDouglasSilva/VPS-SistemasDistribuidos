import threading
from datetime import datetime

class QueueManager:
    def __init__(self):
        self.normal_queue = []
        self.priority_queue = []
        
        self.normal_counter = 0
        self.priority_counter = 0
        self.consecutive_normal_served = 0
        
        self.lock = threading.Lock()
        
    def generate_ticket(self, is_priority: bool) -> str:
        """Gera uma nova senha eletrônica de atendimento (SEA) em ordem crescente."""
        with self.lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if is_priority:
                self.priority_counter += 1
                ticket = f"P{self.priority_counter}"
                self.priority_queue.append(ticket)
                tipo_str = "Prioritário"
            else:
                self.normal_counter += 1
                ticket = f"N{self.normal_counter}"
                self.normal_queue.append(ticket)
                tipo_str = "Normal"
                
            print(f"[{timestamp}] [REGISTRO] Nova senha {ticket} ({tipo_str}) gerada pelo TS.")
            return ticket

    def call_ticket(self, ta_id: str) -> str:
        """Seleciona a próxima senha de acordo com as regras de prioridade."""
        with self.lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Regra Especial: para cada 2 senhas N informadas/chamadas, a próxima é obrigatoriamente P, se houver.
            if self.consecutive_normal_served >= 2 and self.priority_queue:
                ticket = self.priority_queue.pop(0)
                self.consecutive_normal_served = 0
                regra_aplicada = "Regra 2N -> 1P"
            elif self.normal_queue:
                ticket = self.normal_queue.pop(0)
                self.consecutive_normal_served += 1
                regra_aplicada = "Fila Normal"
            elif self.priority_queue:
                ticket = self.priority_queue.pop(0)
                self.consecutive_normal_served = 0
                regra_aplicada = "Fila Prioritária (Normal vazia)"
            else:
                ticket = None
                regra_aplicada = "Filas Vazias"

            if ticket:
                print(f"[{timestamp}] [ATENDIMENTO] Senha {ticket} enviada para {ta_id}. Regra: {regra_aplicada}.")
            else:
                print(f"[{timestamp}] [ATENDIMENTO] Solicitação de {ta_id}, mas nenhuma senha na fila.")
                
            return ticket

    def get_status(self):
        """Retorna o estado atual das filas para exibição ou depuração."""
        with self.lock:
            return {
                "normal_len": len(self.normal_queue),
                "priority_len": len(self.priority_queue),
                "normal_queue": list(self.normal_queue),
                "priority_queue": list(self.priority_queue),
                "consecutive_normal": self.consecutive_normal_served
            }
