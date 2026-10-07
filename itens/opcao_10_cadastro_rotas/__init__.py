"""Opcao 10 do menu: cadastro rotas."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 10 usando a instancia principal do sistema."""
    origem = input("Origem: ")
    destino = input("Destino: ")
    distancia = ler_float("Distância em km: ")
    sistema.rotas.adicionar_aresta(origem, destino, distancia)
    sistema.salvar()
    print("Rota cadastrada.")
