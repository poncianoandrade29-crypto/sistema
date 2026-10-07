"""Opcao 16 do menu: historico."""

def executar(sistema):
    """Executa a opcao 16 usando a instancia principal do sistema."""
    print("\n--- HISTÓRICO ---")
    for item in sistema.historico[-30:]:
        print(item)
