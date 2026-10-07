"""Opcao 6 do menu: despesas."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 6 usando a instancia principal do sistema."""
    categoria = input(
        "Categoria (mudas/insumos/irrigação/"
        "mão de obra/agrônomo/caminhão/outros): "
    )
    descricao = input("Descrição: ")
    valor = ler_float("Valor: R$ ")
    sistema.registrar_despesa(categoria, descricao, valor)
    print("Despesa registrada.")
