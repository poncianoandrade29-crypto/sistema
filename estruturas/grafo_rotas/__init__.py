"""Grafo Rotas data structure."""

from collections import deque

from comum.validacao import validar_numero_nao_negativo


class GrafoRotas:
    """Rotas entre propriedade, galpão, CEASA e outros pontos."""

    def __init__(self):
        """Cria a lista de adjacências que representa as rotas."""
        self.vizinhos = {}

    def adicionar_vertice(self, nome):
        """Registra um ponto sem apagar as ligações que ele já possui."""
        self.vizinhos.setdefault(nome, [])

    def adicionar_aresta(self, origem, destino, distancia_km):
        """Registra uma rota bidirecional entre dois pontos."""
        distancia_km = validar_numero_nao_negativo(
            distancia_km, "A distância da rota"
        )
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self.vizinhos[origem].append((destino, distancia_km))
        self.vizinhos[destino].append((origem, distancia_km))

    def bfs(self, inicio, destino):
        """Encontra um caminho com menos trechos usando busca em largura."""
        if inicio not in self.vizinhos or destino not in self.vizinhos:
            return None

        fila = deque([inicio])
        veio_de = {inicio: None}

        while fila:
            atual = fila.popleft()
            if atual == destino:
                break

            for vizinho, _ in self.vizinhos.get(atual, []):
                if vizinho not in veio_de:
                    veio_de[vizinho] = atual
                    fila.append(vizinho)

        if destino not in veio_de:
            return None

        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = veio_de[atual]
        caminho.reverse()
        return caminho

    def distancia_direta(self, origem, destino):
        """Retorna a distância cadastrada entre vizinhos diretos."""
        for vizinho, distancia in self.vizinhos.get(origem, []):
            if vizinho == destino:
                return distancia
        return None
