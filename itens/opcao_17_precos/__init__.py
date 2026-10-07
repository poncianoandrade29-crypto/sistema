"""Opcao 17 do menu: precos."""

def executar(sistema):
    """Executa a opcao 17 usando a instancia principal do sistema."""
    precos = sistema.arvore_precos.em_ordem()
    if precos:
        print("Preços em ordem:", ", ".join(
            sistema.moeda(x) for x in precos
        ))
    else:
        print("Nenhum preço cadastrado.")
