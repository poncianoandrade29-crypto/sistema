"""Tabela Hash data structure."""

class TabelaHash:
    """Armazena produtos em baldes para localizá-los pelo código."""

    def __init__(self, tamanho=31):
        """Cria os baldes vazios que receberão os pares código-produto."""
        self.tamanho = tamanho
        self.baldes = [[] for _ in range(tamanho)]

    def _hash(self, chave):
        """Converte uma chave em um índice válido da tabela."""
        return sum(ord(c) for c in str(chave)) % self.tamanho

    def inserir(self, chave, valor):
        """Insere ou substitui o produto associado à chave."""
        indice = self._hash(chave)
        for par in self.baldes[indice]:
            if par[0] == chave:
                par[1] = valor
                return
        self.baldes[indice].append([chave, valor])

    def buscar(self, chave):
        """Retorna o valor da chave ou None se ela não estiver cadastrada."""
        indice = self._hash(chave)
        for par in self.baldes[indice]:
            if par[0] == chave:
                return par[1]
        return None

    def remover(self, chave):
        """Remove a chave e informa se ela existia na tabela."""
        indice = self._hash(chave)
        for i, par in enumerate(self.baldes[indice]):
            if par[0] == chave:
                self.baldes[indice].pop(i)
                return True
        return False
