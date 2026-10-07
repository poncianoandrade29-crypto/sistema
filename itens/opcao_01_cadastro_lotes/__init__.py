"""Opcao 1 do menu: cadastro lotes."""

from interface.entrada import ler_float
from interface.entrada import ler_int

def executar(sistema):
    """Executa a opcao 1 usando a instancia principal do sistema."""
    nome = input("Nome/identificação do lote: ")
    area = ler_float("Área em hectares: ")
    mudas = ler_int("Quantidade de mudas: ")
    produtividade = ler_float("Produção estimada por muda (kg): ")
    lote = sistema.cadastrar_lote(nome, area, mudas, produtividade)
    print("Lote cadastrado:", lote)
