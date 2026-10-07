"""Opcao 4 do menu: movimentacao estoque."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 4 usando a instancia principal do sistema."""
    codigo = input("Código do produto: ").upper()
    tipo = input("Tipo (entrada/saida): ").lower()
    qtd = ler_float("Quantidade: ")
    sistema.movimentar_estoque(codigo, qtd, tipo)
    print("Movimentação realizada.")
