"""Opcao 18 do menu: linha do tempo."""

def mostrar_linha_do_tempo(sistema):
    """Exibe as atividades recentes em ordem da mais nova para a mais antiga."""
    print("\n--- LINHA DO TEMPO DAS ATIVIDADES ---")
    atividades = sistema.historico[-100:]
    if not atividades:
        print("Nenhuma atividade registrada.")
        return

    for indice, atividade in enumerate(reversed(atividades)):
        marcador = "└─" if indice == len(atividades) - 1 else "├─"
        print(f"{marcador} {atividade}")

def executar(sistema):
    """Executa a opcao 18 usando a instancia principal do sistema."""
    mostrar_linha_do_tempo(sistema)
