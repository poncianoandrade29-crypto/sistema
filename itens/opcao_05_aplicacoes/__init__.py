"""Opcao 5 do menu: aplicacoes."""

from interface.entrada import ler_int

def executar(sistema):
    """Executa a opcao 5 usando a instancia principal do sistema."""
    lote = ler_int("ID do lote: ")
    codigo = input("Código do produto: ").upper()
    objetivo = input(
        "Objetivo (praga/doença/mato/nutrição/outro): "
    )
    responsavel = input("Responsável/agronomista: ")
    observacao = input(
        "Observação técnica (sem dose/receita): "
    )
    sistema.registrar_aplicacao(
        lote, codigo, objetivo, responsavel, observacao
    )
    print("Aplicação registrada no histórico.")
