import sys
import os
# Adiciona o diretório raiz do projeto ao path do sistema para resolver os imports da pasta 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.srv.modules.queue_manager import QueueManager


class TestQueueManager(unittest.TestCase):
    def setUp(self):
        self.qm = QueueManager()

    def test_ticket_generation_order(self):
        # Gera 3 senhas normais e 2 prioritárias
        n1 = self.qm.generate_ticket(is_priority=False)
        n2 = self.qm.generate_ticket(is_priority=False)
        p1 = self.qm.generate_ticket(is_priority=True)
        n3 = self.qm.generate_ticket(is_priority=False)
        p2 = self.qm.generate_ticket(is_priority=True)

        self.assertEqual(n1, "N1")
        self.assertEqual(n2, "N2")
        self.assertEqual(n3, "N3")
        self.assertEqual(p1, "P1")
        self.assertEqual(p2, "P2")

    def test_scheduling_rule_2n_1p(self):
        # Adiciona senhas na fila
        self.qm.generate_ticket(is_priority=False) # N1
        self.qm.generate_ticket(is_priority=False) # N2
        self.qm.generate_ticket(is_priority=True)  # P1
        self.qm.generate_ticket(is_priority=False) # N3
        self.qm.generate_ticket(is_priority=True)  # P2

        # 1ª chamada: deve ser N1 (consecutive = 1)
        self.assertEqual(self.qm.call_ticket("TA-1"), "N1")
        
        # 2ª chamada: deve ser N2 (consecutive = 2)
        self.assertEqual(self.qm.call_ticket("TA-1"), "N2")
        
        # 3ª chamada: já chamou 2 normais consecutivas e há prioridade (P1 na fila) -> DEVE SER P1 (consecutive reseta para 0)
        self.assertEqual(self.qm.call_ticket("TA-1"), "P1")
        
        # 4ª chamada: consecutive reseta para 0, normal não vazia (N3 na fila) -> DEVE SER N3 (consecutive = 1)
        self.assertEqual(self.qm.call_ticket("TA-1"), "N3")
        
        # 5ª chamada: normal vazia, prioridade não vazia (P2 na fila) -> DEVE SER P2
        self.assertEqual(self.qm.call_ticket("TA-1"), "P2")

        # 6ª chamada: filas vazias -> deve retornar None
        self.assertIsNone(self.qm.call_ticket("TA-1"))

    def test_scheduling_rule_without_priority(self):
        # Apenas senhas normais na fila
        self.qm.generate_ticket(is_priority=False) # N1
        self.qm.generate_ticket(is_priority=False) # N2
        self.qm.generate_ticket(is_priority=False) # N3

        # Chama todas. Mesmo com consecutive >= 2, não há P na fila, então deve continuar chamando as normais
        self.assertEqual(self.qm.call_ticket("TA-1"), "N1")
        self.assertEqual(self.qm.call_ticket("TA-1"), "N2")
        self.assertEqual(self.qm.call_ticket("TA-1"), "N3")
        self.assertIsNone(self.qm.call_ticket("TA-1"))

if __name__ == "__main__":
    unittest.main()
