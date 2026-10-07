"""Opcao 2 do menu: cadastro produtos."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 2 usando a instancia principal do sistema."""
    nome = input("Nome do produto: ")
    categoria = input(
        "Categoria (adubo/defensivo/controle_mato/"
        "irrigacao/embalagem/outro): "
    )
    qtd = ler_float("Quantidade inicial: ")
    custo = ler_float("Custo unitário: ")
    unidade = input("Unidade (kg/L/un/m etc.): ")
    produto = sistema.produto_cadastrar(
        nome, categoria, qtd, custo, unidade
    )
    produto["estoque_minimo"] = ler_float("Estoque mínimo: ")
    sistema.salvar()
    print("Cadastrado:", produto)
