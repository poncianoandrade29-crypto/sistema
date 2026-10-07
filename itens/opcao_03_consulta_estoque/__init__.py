"""Opcao 3 do menu: consulta estoque."""

def executar(sistema):
    """Executa a opcao 3 usando a instancia principal do sistema."""
    print("\n--- ESTOQUE ---")
    for p in sistema.listar_estoque():
        print(
            f"{p['codigo']} | {p['nome']:<28} | "
            f"{p['quantidade']:>10.2f} {p['unidade']} | "
            f"mín.: {p['estoque_minimo']:.2f}"
        )
