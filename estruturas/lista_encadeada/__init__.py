"""Lista Encadeada data structure."""

class NoLista:
    """Nó que guarda um registro e aponta para o próximo nó da lista."""

    def __init__(self, valor):
        """Cria um nó com o valor informado e sem sucessor."""
        self.valor = valor
        self.proximo = None

class ListaEncadeada:
    """Histórico de pulverizações/aplicações."""

    def __init__(self):
        """Inicializa uma lista sem registros."""
        self.inicio = None

    def adicionar(self, valor):
        """Acrescenta um registro ao final da lista encadeada."""
        novo = NoLista(valor)
        if self.inicio is None:
            self.inicio = novo
            return
        atual = self.inicio
        while atual.proximo:
            atual = atual.proximo
        atual.proximo = novo

    def listar(self):
        """Copia os valores da lista para uma lista Python."""
        resultado = []
        atual = self.inicio
        while atual:
            resultado.append(atual.valor)
            atual = atual.proximo
        return resultado
