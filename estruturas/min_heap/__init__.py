"""Min Heap data structure."""

import heapq

class MinHeap:
    """Prioriza tarefas agrícolas e cargas urgentes."""

    def __init__(self):
        """Prepara a heap vazia e o contador que desempata prioridades iguais."""
        self.dados = []
        self.contador = 0

    def inserir(self, prioridade, descricao):
        """Insere uma tarefa; números menores representam maior prioridade."""
        heapq.heappush(self.dados, (prioridade, self.contador, descricao))
        self.contador += 1

    def extrair_min(self):
        """Remove e retorna a tarefa prioritária, ou None se a heap estiver vazia."""
        if not self.dados:
            return None
        return heapq.heappop(self.dados)

    def listar(self):
        """Retorna uma cópia ordenada das tarefas sem alterar a heap."""
        return sorted(self.dados)
