"""Opcao 11 do menu: consulta rotas."""

def executar(sistema):
    """Executa a opcao 11 usando a instancia principal do sistema."""
    origem = input("Origem: ")
    destino = input("Destino: ")
    caminho = sistema.rota(origem, destino)
    if caminho:
        print("Caminho encontrado:", " -> ".join(caminho))
    else:
        print("Não foi encontrado caminho.")
