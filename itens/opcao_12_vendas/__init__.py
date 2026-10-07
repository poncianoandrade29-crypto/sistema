"""Opcao 12 do menu: vendas."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 12 usando a instancia principal do sistema."""
    comprador = input("Comprador: ")
    destino = input("Destino: ")
    quantidade = ler_float("Quantidade vendida (kg): ")
    preco = ler_float("Preço por kg: R$ ")
    frete = ler_float("Frete: R$ ")
    venda = sistema.registrar_venda(
        comprador, destino, quantidade, preco, frete
    )
    print("Venda registrada:", venda)
