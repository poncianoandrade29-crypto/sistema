"""Menu principal do Sistema Tomate."""

from core.sistema import SistemaTomate
from gestao_tomate.cli import menu as menu_gestao_financeira
from itens.opcao_01_cadastro_lotes import executar as opcao_01
from itens.opcao_02_cadastro_produtos import executar as opcao_02
from itens.opcao_03_consulta_estoque import executar as opcao_03
from itens.opcao_04_movimentacao_estoque import executar as opcao_04
from itens.opcao_05_aplicacoes import executar as opcao_05
from itens.opcao_06_despesas import executar as opcao_06
from itens.opcao_07_caminhoes import executar as opcao_07
from itens.opcao_08_fila_cargas import executar as opcao_08
from itens.opcao_09_despacho_cargas import executar as opcao_09
from itens.opcao_10_cadastro_rotas import executar as opcao_10
from itens.opcao_11_consulta_rotas import executar as opcao_11
from itens.opcao_12_vendas import executar as opcao_12
from itens.opcao_13_relatorio import executar as opcao_13
from itens.opcao_14_cadastro_tarefas import executar as opcao_14
from itens.opcao_15_consulta_tarefas import executar as opcao_15
from itens.opcao_16_historico import executar as opcao_16
from itens.opcao_17_precos import executar as opcao_17
from itens.opcao_18_linha_do_tempo import executar as opcao_18
from itens.opcao_19_explorador_arquivos import executar as opcao_19

OPCOES = {
    "1": opcao_01,
    "2": opcao_02,
    "3": opcao_03,
    "4": opcao_04,
    "5": opcao_05,
    "6": opcao_06,
    "7": opcao_07,
    "8": opcao_08,
    "9": opcao_09,
    "10": opcao_10,
    "11": opcao_11,
    "12": opcao_12,
    "13": opcao_13,
    "14": opcao_14,
    "15": opcao_15,
    "16": opcao_16,
    "17": opcao_17,
    "18": opcao_18,
    "19": opcao_19
}


def menu():
    """Exibe o menu e encaminha cada opcao ao seu modulo."""
    sistema = SistemaTomate()
    while True:
        print(
            "\n============================================================\n"
            "        SISTEMA INTEGRADO DE GESTÃO DO TOMATE\n"
            "============================================================\n"
            " 1 - Cadastrar lote / quantidade de mudas\n"
            " 2 - Cadastrar produto/insumo da produção\n"
            " 3 - Ver estoque da produção\n"
            " 4 - Entrada/saída de estoque da produção\n"
            " 5 - Registrar pulverização/aplicação\n"
            " 6 - Registrar despesa da produção\n"
            " 7 - Cadastrar caminhão\n"
            " 8 - Colocar carga na fila\n"
            " 9 - Despachar próxima carga\n"
            "10 - Cadastrar rota\n"
            "11 - Encontrar caminho entre propriedade e CEASA\n"
            "12 - Registrar venda no CEASA\n"
            "13 - Relatório de produção e vendas\n"
            "14 - Adicionar tarefa prioritária\n"
            "15 - Ver/próxima tarefa prioritária\n"
            "16 - Ver histórico\n"
            "17 - Ver preços cadastrados em ordem\n"
            "18 - Ver linha do tempo de atividades\n"
            "19 - Explorar arquivos do sistema\n"
            "20 - Abrir gestão financeira (estoque, compras, despesas, vendas)\n"
            " 0 - Sair\n"
            "============================================================\n"
        )
        opcao = input("Escolha: ").strip()
        try:
            if opcao == "0":
                sistema.salvar()
                print("Dados salvos. Sistema encerrado.")
                break
            if opcao == "20":
                menu_gestao_financeira()
                continue
            executar = OPCOES.get(opcao)
            if executar is None:
                print("Opcao invalida.")
            else:
                executar(sistema)
        except (ValueError, KeyError, TypeError, OSError) as erro:
            print(f"ERRO: {erro}")
        input("\nPressione ENTER para continuar...")
