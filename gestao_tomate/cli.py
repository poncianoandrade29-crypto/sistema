"""Interface de terminal para operar o sistema de gestão do cultivo."""

import sqlite3
from datetime import date

from gestao_tomate.banco import criar_tabelas
from gestao_tomate.servicos import GestaoTomateService


def _ler_texto(mensagem: str) -> str:
    """Solicita um texto obrigatório."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("O valor não pode ficar vazio.")


def _ler_numero(mensagem: str, inteiro: bool = False, zero_permitido: bool = False):
    """Lê números e repete a pergunta se a entrada não for válida."""
    while True:
        try:
            valor = int(input(mensagem)) if inteiro else float(input(mensagem))
            if valor < 0 or (valor == 0 and not zero_permitido):
                print("Informe um valor maior que zero.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Informe um número.")


def _mostrar_menu() -> None:
    """Exibe as operações disponíveis no programa."""
    print("\n=== SISTEMA DE GESTÃO DE CULTIVO DE TOMATE ===")
    print("1. Cadastrar insumo ou muda")
    print("2. Ver estoque")
    print("3. Registrar pulverização/aplicação")
    print("4. Registrar despesa")
    print("5. Cadastrar caminhão")
    print("6. Registrar venda no CEASA")
    print("7. Ver balanço financeiro")
    print("8. Registrar compra/reposição de estoque")
    print("0. Sair")


def menu() -> None:
    """Executa o menu até o usuário escolher sair."""
    criar_tabelas()
    srv = GestaoTomateService()
    while True:
        _mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        hoje = date.today().isoformat()

        try:
            if opcao == "1":
                produto_id = srv.cadastrar_produto(
                    _ler_texto("Nome do produto/insumo: "),
                    _ler_texto("Categoria (remedio, terra, cano, mangueira, muda, outro): "),
                    _ler_numero("Quantidade comprada: "),
                    _ler_texto("Unidade (litros, kg, unidades, metros): "),
                    _ler_numero("Preço unitário (R$): ", zero_permitido=True),
                    hoje,
                )
                print(f"Insumo cadastrado com sucesso (ID {produto_id}).")
            elif opcao == "2":
                estoque = srv.listar_estoque()
                print("\n--- ESTOQUE ATUAL ---")
                if not estoque:
                    print("Nenhum produto cadastrado.")
                for item in estoque:
                    print(
                        f"ID: {item.id} | {item.nome} | {item.categoria} | "
                        f"{item.quantidade:g} {item.unidade} | "
                        f"Preço unitário: R$ {item.preco_unitario:.2f}"
                    )
            elif opcao == "3":
                srv.registrar_pulverizacao(
                    hoje,
                    _ler_numero("ID do produto: ", inteiro=True),
                    _ler_numero("Quantidade aplicada: "),
                    _ler_texto("Identificação da área/talhão: "),
                )
                print("Aplicação registrada e estoque atualizado.")
            elif opcao == "4":
                srv.registrar_despesa(
                    hoje,
                    _ler_texto("Descrição da despesa: "),
                    _ler_texto("Categoria (agronomo, irrigacao, mao_de_obra, outros): "),
                    _ler_numero("Valor total (R$): ", zero_permitido=True),
                )
                print("Despesa registrada com sucesso.")
            elif opcao == "5":
                caminhao_id = srv.cadastrar_caminhao(
                    _ler_texto("Placa do caminhão: "),
                    _ler_texto("Nome do motorista: "),
                    _ler_numero("Capacidade de caixas: ", inteiro=True),
                )
                print(f"Caminhão cadastrado com sucesso (ID {caminhao_id}).")
            elif opcao == "6":
                caminhao_id = _ler_numero(
                    "ID do caminhão (0 para nenhum): ",
                    inteiro=True,
                    zero_permitido=True,
                )
                srv.registrar_venda_ceasa(
                    hoje,
                    caminhao_id or None,
                    _ler_numero("Quantidade de caixas vendidas: ", inteiro=True),
                    _ler_numero("Preço por caixa (R$): ", zero_permitido=True),
                    _ler_numero("Valor do frete/combustível (R$): ", zero_permitido=True),
                )
                print("Venda do CEASA registrada com sucesso.")
            elif opcao == "7":
                resultado = srv.relatorio_financeiro()
                print("\n--- BALANÇO FINANCEIRO DO CULTIVO ---")
                print(f"(-) Compras de insumos/mudas: R$ {resultado['custo_insumos']:.2f}")
                print(f"(-) Despesas gerais:          R$ {resultado['custo_despesas_gerais']:.2f}")
                print(f"(=) Custo total:               R$ {resultado['custo_total']:.2f}")
                print(f"(+) Vendas líquidas no CEASA:  R$ {resultado['faturamento_ceasa']:.2f}")
                situacao = "LUCRO" if resultado["lucro_liquido"] >= 0 else "PREJUÍZO"
                print(f"Resultado ({situacao}):          R$ {resultado['lucro_liquido']:.2f}")
            elif opcao == "8":
                srv.registrar_compra(
                    _ler_numero("ID do produto: ", inteiro=True),
                    _ler_numero("Quantidade comprada: "),
                    _ler_numero("Preço unitário (R$): ", zero_permitido=True),
                    hoje,
                )
                print("Compra registrada e estoque atualizado.")
            elif opcao == "0":
                print("Saindo do sistema...")
                return
            else:
                print("Opção inválida, tente novamente.")
        except ValueError as erro:
            print(f"Não foi possível concluir a operação: {erro}")
        except sqlite3.Error as erro:
            print(f"Erro ao acessar o banco de dados: {erro}")


if __name__ == "__main__":
    menu()
