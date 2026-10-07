"""Opcao 9 do menu: despacho cargas."""

def executar(sistema):
    """Executa a opcao 9 usando a instancia principal do sistema."""
    carga = sistema.despachar_proxima_carga()
    print("Carga despachada:", carga if carga else "fila vazia.")
