"""Arvore Precos data structure."""

class NoBST:
    """Nó da árvore de preços, com referências aos filhos."""

    def __init__(self, valor):
        """Cria um nó de preço sem filhos."""
        self.valor = valor
        self.esquerda = None
        self.direita = None

class BSTPrecos:
    """Árvore para organizar preços de venda."""

    def __init__(self):
        """Inicializa uma árvore binária de busca vazia."""
        self.raiz = None

    def inserir(self, valor):
        """Insere um preço sem recursão e preserva preços repetidos."""
        if self.raiz is None:
            self.raiz = NoBST(valor)
            return

        atual = self.raiz
        while True:
            if valor < atual.valor:
                if atual.esquerda is None:
                    atual.esquerda = NoBST(valor)
                    return
                atual = atual.esquerda
            else:
                if atual.direita is None:
                    atual.direita = NoBST(valor)
                    return
                atual = atual.direita

    def _inserir(self, no, valor):
        """Insere a partir de um nó informado sem exceder a pilha de chamadas."""
        atual = no
        while True:
            if valor < atual.valor:
                if atual.esquerda is None:
                    atual.esquerda = NoBST(valor)
                    return
                atual = atual.esquerda
            else:
                if atual.direita is None:
                    atual.direita = NoBST(valor)
                    return
                atual = atual.direita

    def em_ordem(self, no=None, resultado=None):
        """Devolve os preços em ordem crescente, incluindo valores repetidos."""
        if resultado is None:
            resultado = []

        # A pilha explícita evita recursão infinita em filhos inexistentes e
        # também suporta árvores desbalanceadas com muitos preços.
        pilha = []
        atual = self.raiz if no is None else no
        while pilha or atual is not None:
            while atual is not None:
                pilha.append(atual)
                atual = atual.esquerda
            atual = pilha.pop()
            resultado.append(atual.valor)
            atual = atual.direita
        return resultado
